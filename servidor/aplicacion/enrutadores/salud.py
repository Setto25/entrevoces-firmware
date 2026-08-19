"""Expone la comprobación de salud del backend."""

from fastapi import APIRouter

from aplicacion.esquemas.respuestas import RespuestaSalud


enrutador: APIRouter = APIRouter(tags=["salud"])


@enrutador.get("/salud", response_model=RespuestaSalud)
def consultar_salud() -> RespuestaSalud:
    """Confirma que la versión activa de la API responde."""
    return RespuestaSalud(estado="saludable", servicio="entrevoces", version_api="v1")
