"""Configura la aplicación HTTP principal de EntreVoces."""

from fastapi import FastAPI

from aplicacion.enrutadores.audios import enrutador as enrutador_audios
from aplicacion.enrutadores.salud import enrutador as enrutador_salud
from aplicacion.enrutadores.sesiones import enrutador as enrutador_sesiones


def crear_aplicacion() -> FastAPI:
    """Crea la aplicación y registra los enrutadores de la versión activa."""
    instancia: FastAPI = FastAPI(
        title="EntreVoces",
        description="API del MVP de comunicación por voz de EntreVoces",
        version="0.1.0",
    )
    instancia.include_router(enrutador_salud, prefix="/api/v1")
    instancia.include_router(enrutador_audios, prefix="/api/v1")
    instancia.include_router(enrutador_sesiones, prefix="/api/v1")
    return instancia


aplicacion: FastAPI = crear_aplicacion()
