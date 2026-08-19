"""Ejecuta un turno HTTP del simulador contra el contrato de EntreVoces."""

from __future__ import annotations

import argparse
import json
import math
import mimetypes
import os
import struct
import sys
import wave
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from uuid import uuid4

from wokwi_dispositivo.nucleo_estados import ControladorEstados


TIEMPO_ESPERA_PREDETERMINADO_SEGUNDOS: float = 10.0
TIPO_WAV: str = "audio/wav"


class ErrorComunicacion(RuntimeError):
    """Representa un fallo de transporte contra el servidor."""


class ErrorRespuesta(RuntimeError):
    """Representa una respuesta que incumple el contrato del simulador."""


class TransporteHttp(Protocol):
    """Define la operación HTTP mínima necesaria para el simulador."""

    def enviar(self, solicitud: Request, tiempo_espera_segundos: float) -> tuple[int, bytes, str]:
        """Envía una solicitud y devuelve estado, contenido y tipo declarado."""


@dataclass(frozen=True)
class ResultadoTurno:
    """Describe el resultado observable de un turno simulado."""

    estado_final: str
    identificador_correlacion: str
    ruta_audio_descargado: Path


class TransporteUrllib:
    """Adapta urllib para el transporte HTTP real del simulador."""

    def enviar(self, solicitud: Request, tiempo_espera_segundos: float) -> tuple[int, bytes, str]:
        """Ejecuta la solicitud HTTP y normaliza los errores de red."""
        try:
            with urlopen(solicitud, timeout=tiempo_espera_segundos) as respuesta:
                tipo_contenido: str = respuesta.headers.get_content_type()
                return respuesta.status, respuesta.read(), tipo_contenido
        except HTTPError as error:
            detalle: bytes = error.read()
            raise ErrorComunicacion(
                f"El servidor respondió HTTP {error.code}: {detalle.decode(errors='replace')}"
            ) from error
        except (TimeoutError, URLError, OSError) as error:
            raise ErrorComunicacion(f"No se pudo comunicar con el servidor: {error}") from error


class ClienteHttpSimulador:
    """Coordina un turno de audio del simulador mediante HTTP por archivo completo."""

    def __init__(
        self,
        url_base: str,
        credencial_dispositivo: str,
        transporte: TransporteHttp | None = None,
        tiempo_espera_segundos: float = TIEMPO_ESPERA_PREDETERMINADO_SEGUNDOS,
    ) -> None:
        """Inicializa el cliente con una URL base y transporte intercambiable."""
        self._url_base: str = url_base.rstrip("/") + "/"
        self._credencial_dispositivo: str = credencial_dispositivo
        self._transporte: TransporteHttp = transporte or TransporteUrllib()
        self._tiempo_espera_segundos: float = tiempo_espera_segundos
        self.controlador: ControladorEstados = ControladorEstados()

    def ejecutar_turno(self, ruta_audio_entrada: Path, ruta_audio_salida: Path) -> ResultadoTurno:
        """Envía un WAV, descarga la respuesta y devuelve el simulador a listo."""
        identificador_correlacion: str = str(uuid4())
        token_sesion: str | None = None
        self.controlador.iniciar()
        try:
            token_sesion = self._iniciar_sesion()
            datos_audio: bytes = ruta_audio_entrada.read_bytes()
            _validar_wav(datos_audio)
            self.controlador.transicionar("BOTON_PRESIONADO")
            self.controlador.transicionar("BOTON_SOLTADO")
            cuerpo, limite = _crear_multipart(datos_audio, ruta_audio_entrada.name)
            solicitud_turno: Request = Request(
                urljoin(self._url_base, "api/v1/turnos/audio"),
                data=cuerpo,
                headers={
                    "Content-Type": f"multipart/form-data; boundary={limite}",
                    "X-Id-Correlacion": identificador_correlacion,
                    "X-Sesion-Dispositivo": token_sesion,
                },
                method="POST",
            )
            estado, contenido, tipo_contenido = self._transporte.enviar(
                solicitud_turno, self._tiempo_espera_segundos
            )
            if estado != 201 or tipo_contenido != "application/json":
                raise ErrorRespuesta("La respuesta del turno no tiene el estado o tipo esperado.")
            self.controlador.transicionar("ENVIO_CONFIRMADO")
            ruta_audio: str = _extraer_ruta_audio(contenido)
            solicitud_audio: Request = Request(urljoin(self._url_base, ruta_audio.lstrip("/")))
            estado_audio, datos_respuesta, tipo_audio = self._transporte.enviar(
                solicitud_audio, self._tiempo_espera_segundos
            )
            if estado_audio != 200 or tipo_audio != TIPO_WAV:
                raise ErrorRespuesta("La descarga de audio no tiene el estado o tipo esperado.")
            _validar_wav(datos_respuesta)
            ruta_audio_salida.parent.mkdir(parents=True, exist_ok=True)
            ruta_audio_salida.write_bytes(datos_respuesta)
            self._cerrar_sesion(token_sesion)
            token_sesion = None
            self.controlador.transicionar("RESPUESTA_LISTA")
            self.controlador.transicionar("REPRODUCCION_FINALIZADA")
            return ResultadoTurno(
                estado_final=self.controlador.estado_actual,
                identificador_correlacion=identificador_correlacion,
                ruta_audio_descargado=ruta_audio_salida,
            )
        except (ErrorComunicacion, ErrorRespuesta, TimeoutError, OSError, wave.Error, ValueError):
            if token_sesion is not None:
                try:
                    self._cerrar_sesion(token_sesion)
                except ErrorComunicacion:
                    pass
            self.controlador.transicionar("FALLO")
            self.controlador.transicionar("REINTENTAR")
            raise

    def _iniciar_sesion(self) -> str:
        """Inicia una sesión temporal usando la credencial configurada del dispositivo."""
        if not self._credencial_dispositivo:
            raise ErrorRespuesta("Falta la credencial del dispositivo en el simulador.")
        solicitud: Request = Request(
            urljoin(self._url_base, "api/v1/sesiones/dispositivo/iniciar"),
            headers={"X-Credencial-Dispositivo": self._credencial_dispositivo},
            method="POST",
        )
        estado, contenido, tipo_contenido = self._transporte.enviar(
            solicitud, self._tiempo_espera_segundos
        )
        if estado != 201 or tipo_contenido != "application/json":
            raise ErrorRespuesta("No se pudo iniciar una sesión de dispositivo válida.")
        try:
            respuesta: object = json.loads(contenido)
            if not isinstance(respuesta, dict):
                raise ValueError("El cuerpo no es un objeto JSON.")
            token_sesion: object = respuesta.get("token_sesion")
            if not isinstance(token_sesion, str) or not token_sesion:
                raise ValueError("La sesión no contiene un token válido.")
            return token_sesion
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
            raise ErrorRespuesta(f"El JSON de sesión es inválido: {error}") from error

    def _cerrar_sesion(self, token_sesion: str) -> None:
        """Revoca la sesión temporal después de completar o abortar el turno."""
        solicitud: Request = Request(
            urljoin(self._url_base, "api/v1/sesiones/dispositivo/cerrar"),
            headers={"X-Sesion-Dispositivo": token_sesion},
            method="POST",
        )
        estado, _, _ = self._transporte.enviar(solicitud, self._tiempo_espera_segundos)
        if estado != 204:
            raise ErrorRespuesta("No se pudo cerrar la sesión del dispositivo.")


def generar_wav_controlado(ruta_audio: Path, duracion_segundos: float = 0.25) -> None:
    """Genera un WAV PCM controlado para probar el transporte local."""
    cantidad_muestras: int = round(16_000 * duracion_segundos)
    contenido: BytesIO = BytesIO()
    with wave.open(contenido, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(16_000)
        for indice in range(cantidad_muestras):
            muestra: int = round(5_000 * math.sin(2 * math.pi * 440 * indice / 16_000))
            archivo.writeframesraw(struct.pack("<h", muestra))
    ruta_audio.parent.mkdir(parents=True, exist_ok=True)
    ruta_audio.write_bytes(contenido.getvalue())


def _crear_multipart(datos_audio: bytes, nombre_archivo: str) -> tuple[bytes, str]:
    """Construye el formulario multipart para el campo de audio del contrato."""
    limite: str = f"----EntreVoces{uuid4().hex}"
    cabecera: bytes = (
        f"--{limite}\r\n"
        f'Content-Disposition: form-data; name="audio"; filename="{nombre_archivo}"\r\n'
        f"Content-Type: {TIPO_WAV}\r\n\r\n"
    ).encode()
    return cabecera + datos_audio + f"\r\n--{limite}--\r\n".encode(), limite


def _extraer_ruta_audio(contenido: bytes) -> str:
    """Extrae y valida el único comando reproducible admitido por el simulador."""
    try:
        respuesta: object = json.loads(contenido)
        if not isinstance(respuesta, dict):
            raise ValueError("El cuerpo no es un objeto JSON.")
        comandos: object = respuesta.get("comandos")
        if not isinstance(comandos, list) or len(comandos) != 1:
            raise ValueError("La respuesta debe contener un comando.")
        comando: object = comandos[0]
        if not isinstance(comando, dict) or comando.get("tipo") != "REPRODUCIR_AUDIO":
            raise ValueError("El comando no permite reproducir audio.")
        ruta_audio: object = comando.get("ruta_audio")
        if not isinstance(ruta_audio, str) or not ruta_audio.startswith("/"):
            raise ValueError("La ruta del audio no es válida.")
        return ruta_audio
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise ErrorRespuesta(f"El JSON del turno es inválido: {error}") from error


def _validar_wav(datos_audio: bytes) -> None:
    """Comprueba que un WAV cumple PCM mono de 16 kHz y 16 bits."""
    with wave.open(BytesIO(datos_audio), "rb") as archivo:
        if (
            archivo.getcomptype() != "NONE"
            or archivo.getnchannels() != 1
            or archivo.getframerate() != 16_000
            or archivo.getsampwidth() != 2
            or archivo.getnframes() <= 0
        ):
            raise ValueError("El WAV debe ser PCM mono de 16 kHz, 16 bits y no vacío.")


def reproducir_audio(ruta_audio: Path) -> None:
    """Reproduce el WAV descargado cuando el sistema operativo lo permite."""
    if sys.platform != "win32":
        raise OSError("La reproducción automática solo está disponible en Windows.")
    import winsound

    winsound.PlaySound(str(ruta_audio), winsound.SND_FILENAME)


def crear_analizador() -> argparse.ArgumentParser:
    """Crea los argumentos de ejecución del simulador HTTP."""
    analizador: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Envía un WAV al backend y descarga su respuesta."
    )
    analizador.add_argument("--url-base", default="http://127.0.0.1:8000")
    analizador.add_argument("--entrada", type=Path, default=Path("audio_entrada.wav"))
    analizador.add_argument("--salida", type=Path, default=Path("audio_respuesta.wav"))
    analizador.add_argument("--generar-entrada", action="store_true")
    analizador.add_argument("--reproducir", action="store_true")
    analizador.add_argument(
        "--credencial-dispositivo", default=os.getenv("ENTREVOCES_CREDENCIAL_DISPOSITIVO", "")
    )
    return analizador


def main() -> int:
    """Ejecuta el turno solicitado e informa el resultado observable."""
    argumentos: argparse.Namespace = crear_analizador().parse_args()
    if argumentos.generar_entrada:
        generar_wav_controlado(argumentos.entrada)
    try:
        resultado: ResultadoTurno = ClienteHttpSimulador(
            argumentos.url_base, argumentos.credencial_dispositivo
        ).ejecutar_turno(argumentos.entrada, argumentos.salida)
    except (ErrorComunicacion, ErrorRespuesta, OSError, wave.Error, ValueError) as error:
        print(f"ERROR: {error}")
        return 1
    if argumentos.reproducir:
        try:
            reproducir_audio(resultado.ruta_audio_descargado)
        except OSError as error:
            print(f"ERROR: {error}")
            return 1
    print(f"Estado final: {resultado.estado_final}")
    print(f"Correlación: {resultado.identificador_correlacion}")
    print(f"Audio descargado: {resultado.ruta_audio_descargado.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
