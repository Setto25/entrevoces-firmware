"""Define los contratos de respuesta de la API del dispositivo."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class RespuestaSalud(BaseModel):
    """Describe el estado observable del servicio."""

    estado: Literal["saludable"]
    servicio: Literal["entrevoces"]
    version_api: Literal["v1"]


class RespuestaInicioSesion(BaseModel):
    """Describe una sesión temporal emitida para un dispositivo autenticado."""

    token_sesion: str = Field(min_length=1)
    expira_en_segundos: int = Field(gt=0)


class MetadatosAudio(BaseModel):
    """Describe las propiedades verificadas de un audio recibido."""

    canales: int = Field(ge=1)
    frecuencia_hz: int = Field(gt=0)
    bits_por_muestra: int = Field(gt=0)
    duracion_ms: int = Field(ge=0)
    bytes_recibidos: int = Field(gt=0)


class ComandoDispositivo(BaseModel):
    """Indica una acción cerrada que el dispositivo puede ejecutar."""

    tipo: Literal["REPRODUCIR_AUDIO"]
    ruta_audio: str


class RespuestaTurno(BaseModel):
    """Representa el resultado mínimo de un turno de voz."""

    identificador_turno: UUID
    identificador_correlacion: str
    estado: Literal["procesado"]
    audio_entrada: MetadatosAudio
    comandos: list[ComandoDispositivo]
