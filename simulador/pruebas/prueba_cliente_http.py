"""Verifica el comportamiento recuperable del cliente HTTP del simulador."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.request import Request


RUTA_SIMULADOR: Path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUTA_SIMULADOR))
sys.modules.pop("cliente_http", None)

from cliente_http import ClienteHttpSimulador, ErrorComunicacion, ErrorRespuesta, generar_wav_controlado


class TransporteControlado:
    """Entrega respuestas controladas para aislar el cliente HTTP."""

    def __init__(self, respuestas: list[tuple[int, bytes, str] | Exception]) -> None:
        """Conserva la secuencia de respuestas preparada por cada prueba."""
        self.respuestas: list[tuple[int, bytes, str] | Exception] = respuestas
        self.solicitudes: list[Request] = []

    def enviar(self, solicitud: Request, tiempo_espera_segundos: float) -> tuple[int, bytes, str]:
        """Devuelve la siguiente respuesta o propaga el fallo configurado."""
        self.solicitudes.append(solicitud)
        resultado: tuple[int, bytes, str] | Exception = self.respuestas.pop(0)
        if isinstance(resultado, Exception):
            raise resultado
        return resultado


class PruebaClienteHttpSimulador(unittest.TestCase):
    """Comprueba el turno completo y su recuperación ante errores."""

    def setUp(self) -> None:
        """Prepara archivos WAV aislados para cada caso de prueba."""
        self.directorio_temporal: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
        self.directorio: Path = Path(self.directorio_temporal.name)
        self.entrada: Path = self.directorio / "entrada.wav"
        generar_wav_controlado(self.entrada)

    def tearDown(self) -> None:
        """Libera los archivos temporales generados durante la prueba."""
        self.directorio_temporal.cleanup()

    def test_turno_descarga_audio_y_vuelve_a_listo(self) -> None:
        """Comprueba que el comando válido termina con un WAV descargado."""
        respuesta_turno: bytes = json.dumps(
            {"comandos": [{"tipo": "REPRODUCIR_AUDIO", "ruta_audio": "/api/v1/audios/respuesta-fija"}]}
        ).encode()
        transporte: TransporteControlado = TransporteControlado(
            [
                (201, b'{"token_sesion":"sesion-prueba"}', "application/json"),
                (201, respuesta_turno, "application/json"),
                (200, self.entrada.read_bytes(), "audio/wav"),
                (204, b"", "text/plain"),
            ]
        )

        resultado = ClienteHttpSimulador(
            "http://servidor.local", "credencial-prueba", transporte
        ).ejecutar_turno(self.entrada, self.directorio / "respuesta.wav")

        self.assertEqual(resultado.estado_final, "LISTO")
        self.assertTrue(resultado.ruta_audio_descargado.exists())
        self.assertEqual(len(transporte.solicitudes), 4)
        self.assertEqual(transporte.solicitudes[1].get_method(), "POST")

    def test_respuesta_invalida_recupera_listo(self) -> None:
        """Comprueba que un comando inválido deja el controlador recuperado."""
        transporte: TransporteControlado = TransporteControlado(
            [
                (201, b'{"token_sesion":"sesion-prueba"}', "application/json"),
                (201, b"{}", "application/json"),
                (204, b"", "text/plain"),
            ]
        )
        cliente: ClienteHttpSimulador = ClienteHttpSimulador(
            "http://servidor.local", "credencial-prueba", transporte
        )

        with self.assertRaises(ErrorRespuesta):
            cliente.ejecutar_turno(self.entrada, self.directorio / "respuesta.wav")

        self.assertEqual(cliente.controlador.estado_actual, "LISTO")

    def test_fallo_de_red_recupera_listo(self) -> None:
        """Comprueba que una pérdida de red deja el controlador recuperado."""
        transporte: TransporteControlado = TransporteControlado([ErrorComunicacion("sin red")])
        cliente: ClienteHttpSimulador = ClienteHttpSimulador(
            "http://servidor.local", "credencial-prueba", transporte
        )

        with self.assertRaises(ErrorComunicacion):
            cliente.ejecutar_turno(self.entrada, self.directorio / "respuesta.wav")

        self.assertEqual(cliente.controlador.estado_actual, "LISTO")

    def test_timeout_recupera_listo(self) -> None:
        """Comprueba que un timeout deja el controlador recuperado."""
        transporte: TransporteControlado = TransporteControlado([TimeoutError("agotado")])
        cliente: ClienteHttpSimulador = ClienteHttpSimulador(
            "http://servidor.local", "credencial-prueba", transporte
        )

        with self.assertRaises(TimeoutError):
            cliente.ejecutar_turno(self.entrada, self.directorio / "respuesta.wav")

        self.assertEqual(cliente.controlador.estado_actual, "LISTO")
