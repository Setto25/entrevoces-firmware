"""Expone el contrato HTTP inicial para turnos de audio."""

from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, File, Header, HTTPException, Response, UploadFile, status

from aplicacion.esquemas.respuestas import ComandoDispositivo, RespuestaTurno
from aplicacion.servicios.audios import (
    LIMITE_AUDIO_BYTES,
    ErrorContratoAudio,
    generar_audio_respuesta,
    inspeccionar_wav,
)
from aplicacion.servicios.sesiones_dispositivo import (
    ErrorSesionDispositivo,
    gestor_sesiones_dispositivo,
)


enrutador: APIRouter = APIRouter(tags=["audio"])
TIPOS_WAV_PERMITIDOS: frozenset[str] = frozenset({"audio/wav", "audio/x-wav", "audio/wave"})


@enrutador.get("/audios/respuesta-fija")
def descargar_audio_respuesta() -> Response:
    """Entrega un WAV fijo para comprobar la reproducción del cliente."""
    return Response(
        content=generar_audio_respuesta(),
        media_type="audio/wav",
        headers={"Content-Disposition": 'attachment; filename="respuesta_entrevoces.wav"'},
    )


@enrutador.post("/turnos/audio", response_model=RespuestaTurno, status_code=status.HTTP_201_CREATED)
async def procesar_turno_audio(
    respuesta_http: Response,
    audio: Annotated[UploadFile, File(description="WAV PCM mono, 16000 Hz y 16 bits")],
    identificador_solicitud: Annotated[
        str | None,
        Header(alias="X-Id-Correlacion", max_length=100),
    ] = None,
    token_sesion: Annotated[
        str | None, Header(alias="X-Sesion-Dispositivo", min_length=1, max_length=512)
    ] = None,
) -> RespuestaTurno:
    """Valida un audio completo y devuelve un comando determinista de reproducción."""
    try:
        gestor_sesiones_dispositivo.validar(token_sesion or "")
    except ErrorSesionDispositivo as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"codigo": "sesion_dispositivo_invalida", "mensaje": "La sesión no es válida."},
        ) from error
    if audio.content_type not in TIPOS_WAV_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"codigo": "tipo_audio_no_permitido", "mensaje": "Se requiere audio/wav."},
        )

    datos: bytes = await audio.read(LIMITE_AUDIO_BYTES + 1)
    await audio.close()
    if len(datos) > LIMITE_AUDIO_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail={"codigo": "audio_demasiado_grande", "mensaje": "El audio supera 2 MiB."},
        )

    try:
        metadatos = inspeccionar_wav(datos)
    except ErrorContratoAudio as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"codigo": "wav_invalido", "mensaje": str(error)},
        ) from error

    correlacion: str = identificador_solicitud or str(uuid4())
    respuesta_http.headers["X-Id-Correlacion"] = correlacion
    return RespuestaTurno(
        identificador_turno=uuid4(),
        identificador_correlacion=correlacion,
        estado="procesado",
        audio_entrada=metadatos,
        comandos=[
            ComandoDispositivo(
                tipo="REPRODUCIR_AUDIO",
                ruta_audio="/api/v1/audios/respuesta-fija",
            )
        ],
    )
