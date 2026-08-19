"""Expone el inicio y cierre de sesión del dispositivo."""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response, status

from aplicacion.esquemas.respuestas import RespuestaInicioSesion
from aplicacion.servicios.sesiones_dispositivo import (
    DURACION_SESION_SEGUNDOS,
    ErrorConfiguracionSesion,
    ErrorCredencialDispositivo,
    ErrorSesionDispositivo,
    gestor_sesiones_dispositivo,
)


enrutador: APIRouter = APIRouter(tags=["sesiones"])


@enrutador.post(
    "/sesiones/dispositivo/iniciar",
    response_model=RespuestaInicioSesion,
    status_code=status.HTTP_201_CREATED,
)
def iniciar_sesion_dispositivo(
    credencial_dispositivo: Annotated[
        str, Header(alias="X-Credencial-Dispositivo", min_length=1, max_length=512)
    ],
) -> RespuestaInicioSesion:
    """Emite una sesión temporal después de validar la credencial del dispositivo."""
    try:
        sesion = gestor_sesiones_dispositivo.iniciar(credencial_dispositivo)
    except ErrorConfiguracionSesion as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "credencial_dispositivo_no_configurada", "mensaje": str(error)},
        ) from error
    except ErrorCredencialDispositivo as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"codigo": "credencial_dispositivo_invalida", "mensaje": "No se pudo autenticar el dispositivo."},
        ) from error
    return RespuestaInicioSesion(token_sesion=sesion.token, expira_en_segundos=DURACION_SESION_SEGUNDOS)


@enrutador.post("/sesiones/dispositivo/cerrar", status_code=status.HTTP_204_NO_CONTENT)
def cerrar_sesion_dispositivo(
    token_sesion: Annotated[
        str, Header(alias="X-Sesion-Dispositivo", min_length=1, max_length=512)
    ],
) -> Response:
    """Revoca la sesión temporal asociada al dispositivo autenticado."""
    try:
        gestor_sesiones_dispositivo.cerrar(token_sesion)
    except ErrorSesionDispositivo as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"codigo": "sesion_dispositivo_invalida", "mensaje": "La sesión no es válida."},
        ) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
