"""Verifica el cliente HTTP de MicroPython mediante un transporte controlado."""

import json
import sys
import unittest
from pathlib import Path


RUTA_MICROPYTHON: Path = Path(__file__).resolve().parents[1] / "micropython"
sys.path.insert(0, str(RUTA_MICROPYTHON))

from cliente_http import ClienteHttpDispositivo, ErrorContrato, ErrorRed
from controlador_turno import ControladorTurno
from nucleo_estados import ControladorEstados


class RespuestaControlada:
    """Representa una respuesta mínima compatible con urequests."""

    def __init__(self, estado: int, contenido: bytes) -> None:
        """Conserva un estado y contenido deterministas para la prueba."""
        self.status_code: int = estado
        self.content: bytes = contenido
        self.cerrada: bool = False

    def close(self) -> None:
        """Marca la respuesta como cerrada para comprobar liberación de recursos."""
        self.cerrada = True


class TransporteControlado:
    """Entrega respuestas controladas siguiendo la secuencia del contrato."""

    def __init__(self, respuestas: list[RespuestaControlada | Exception]) -> None:
        """Conserva las respuestas que consumirá el cliente en cada solicitud."""
        self.respuestas: list[RespuestaControlada | Exception] = respuestas
        self.solicitudes: list[dict[str, object]] = []

    def post(self, url: str, data: bytes, headers: dict[str, str], timeout: int) -> RespuestaControlada:
        """Registra una solicitud POST y entrega su respuesta preparada."""
        return self._responder("POST", url, data, headers, timeout)

    def get(self, url: str, data: bytes, headers: dict[str, str], timeout: int) -> RespuestaControlada:
        """Registra una solicitud GET y entrega su respuesta preparada."""
        return self._responder("GET", url, data, headers, timeout)

    def _responder(
        self, metodo: str, url: str, data: bytes, headers: dict[str, str], timeout: int
    ) -> RespuestaControlada:
        """Extrae la siguiente respuesta o propaga el fallo configurado."""
        self.solicitudes.append({"metodo": metodo, "url": url, "headers": headers})
        resultado: RespuestaControlada | Exception = self.respuestas.pop(0)
        if isinstance(resultado, Exception):
            raise resultado
        return resultado


def crear_wav() -> bytes:
    """Genera una cabecera WAV mínima suficiente para el contrato actual."""
    return b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 32


class PruebaClienteHttpDispositivo(unittest.TestCase):
    """Comprueba sesión, turno y recuperación del cliente de firmware."""

    def test_turno_inicia_y_cierra_sesion(self) -> None:
        """Comprueba que el recorrido usa sesión temporal y devuelve un WAV."""
        respuesta_turno: bytes = json.dumps(
            {"comandos": [{"tipo": "REPRODUCIR_AUDIO", "ruta_audio": "/api/v1/audios/respuesta-fija"}]}
        ).encode()
        transporte: TransporteControlado = TransporteControlado(
            [
                RespuestaControlada(201, b'{"token_sesion":"sesion-temporal"}'),
                RespuestaControlada(201, respuesta_turno),
                RespuestaControlada(200, crear_wav()),
                RespuestaControlada(204, b""),
            ]
        )
        cliente: ClienteHttpDispositivo = ClienteHttpDispositivo(
            "http://servidor.local", "credencial-local", transporte
        )

        audio: bytes = cliente.ejecutar_turno(crear_wav(), "correlacion-001")

        self.assertEqual(audio, crear_wav())
        self.assertEqual(len(transporte.solicitudes), 4)
        self.assertEqual(transporte.solicitudes[1]["headers"]["X-Sesion-Dispositivo"], "sesion-temporal")

    def test_fallo_de_red_cierra_sesion_y_controlador_recupera_listo(self) -> None:
        """Comprueba que un fallo de red no deja el firmware bloqueado."""
        transporte: TransporteControlado = TransporteControlado(
            [
                RespuestaControlada(201, b'{"token_sesion":"sesion-temporal"}'),
                OSError("sin red"),
                RespuestaControlada(204, b""),
            ]
        )
        cliente: ClienteHttpDispositivo = ClienteHttpDispositivo(
            "http://servidor.local", "credencial-local", transporte
        )
        estados: ControladorEstados = ControladorEstados()
        estados.iniciar()
        estados.transicionar("BOTON_PRESIONADO")
        estados.transicionar("BOTON_SOLTADO")
        controlador: ControladorTurno = ControladorTurno(estados, cliente)

        with self.assertRaises(ErrorRed):
            controlador.enviar_audio(crear_wav(), "correlacion-002")

        self.assertEqual(estados.estado_actual, estados.LISTO)

    def test_comando_desconocido_se_rechaza(self) -> None:
        """Comprueba que el firmware no ejecuta comandos fuera del contrato."""
        transporte: TransporteControlado = TransporteControlado(
            [
                RespuestaControlada(201, b'{"token_sesion":"sesion-temporal"}'),
                RespuestaControlada(201, b'{"comandos":[{"tipo":"BORRAR"}]}'),
                RespuestaControlada(204, b""),
            ]
        )
        cliente: ClienteHttpDispositivo = ClienteHttpDispositivo(
            "http://servidor.local", "credencial-local", transporte
        )

        with self.assertRaises(ErrorContrato):
            cliente.ejecutar_turno(crear_wav(), "correlacion-003")
