"""Verifica el simulador HTTP contra la aplicación FastAPI real."""

import sys
import tempfile
import os
from pathlib import Path
from urllib.request import Request

from fastapi.testclient import TestClient

from aplicacion.aplicacion import aplicacion


RUTA_SIMULADOR: Path = Path(__file__).resolve().parents[2] / "simulador"
sys.path.insert(0, str(RUTA_SIMULADOR))

from cliente_http import ClienteHttpSimulador, generar_wav_controlado


class TransporteAplicacion:
    """Adapta TestClient al transporte esperado por el simulador."""

    def __init__(self) -> None:
        """Inicializa el cliente HTTP en memoria de FastAPI."""
        self.cliente: TestClient = TestClient(aplicacion)

    def enviar(self, solicitud: Request, tiempo_espera_segundos: float) -> tuple[int, bytes, str]:
        """Envía la solicitud al ASGI real sin abrir un puerto de red."""
        respuesta = self.cliente.request(
            method=solicitud.get_method(),
            url=solicitud.full_url,
            content=solicitud.data,
            headers=dict(solicitud.header_items()),
        )
        return (
            respuesta.status_code,
            respuesta.content,
            respuesta.headers.get("content-type", "").split(";")[0],
        )


def test_simulador_completa_turno_con_backend_real() -> None:
    """Comprueba que simulador y backend comparten el contrato HTTP v1."""
    os.environ["ENTREVOCES_CREDENCIAL_DISPOSITIVO"] = "credencial-integracion"
    with tempfile.TemporaryDirectory() as directorio:
        ruta_directorio: Path = Path(directorio)
        entrada: Path = ruta_directorio / "entrada.wav"
        salida: Path = ruta_directorio / "respuesta.wav"
        generar_wav_controlado(entrada)

        resultado = ClienteHttpSimulador(
            "http://prueba.local", "credencial-integracion", TransporteAplicacion()
        ).ejecutar_turno(entrada, salida)

        assert resultado.estado_final == "LISTO"
        assert salida.exists()
        assert salida.stat().st_size > 44
