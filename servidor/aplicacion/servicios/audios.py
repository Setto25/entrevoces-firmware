"""Valida y genera audios del contrato inicial de EntreVoces."""

import math
import struct
import wave
from io import BytesIO

from aplicacion.esquemas.respuestas import MetadatosAudio


FRECUENCIA_REQUERIDA_HZ: int = 16_000
CANALES_REQUERIDOS: int = 1
BITS_REQUERIDOS: int = 16
LIMITE_AUDIO_BYTES: int = 2 * 1024 * 1024


class ErrorContratoAudio(ValueError):
    """Representa un WAV que no cumple el contrato del dispositivo."""


def inspeccionar_wav(datos: bytes) -> MetadatosAudio:
    """Valida el contenedor WAV y devuelve sus propiedades verificadas."""
    try:
        with wave.open(BytesIO(datos), "rb") as archivo:
            canales: int = archivo.getnchannels()
            ancho_muestra: int = archivo.getsampwidth()
            frecuencia_hz: int = archivo.getframerate()
            fotogramas: int = archivo.getnframes()
            compresion: str = archivo.getcomptype()
    except (EOFError, wave.Error) as error:
        raise ErrorContratoAudio("El archivo no contiene un WAV legible.") from error

    bits_por_muestra: int = ancho_muestra * 8
    if compresion != "NONE":
        raise ErrorContratoAudio("El WAV debe usar PCM sin compresión.")
    if canales != CANALES_REQUERIDOS:
        raise ErrorContratoAudio("El WAV debe ser mono.")
    if frecuencia_hz != FRECUENCIA_REQUERIDA_HZ:
        raise ErrorContratoAudio("El WAV debe usar una frecuencia de 16000 Hz.")
    if bits_por_muestra != BITS_REQUERIDOS:
        raise ErrorContratoAudio("El WAV debe usar muestras de 16 bits.")

    duracion_ms: int = round((fotogramas / frecuencia_hz) * 1000)
    return MetadatosAudio(
        canales=canales,
        frecuencia_hz=frecuencia_hz,
        bits_por_muestra=bits_por_muestra,
        duracion_ms=duracion_ms,
        bytes_recibidos=len(datos),
    )


def generar_audio_respuesta() -> bytes:
    """Genera un tono WAV fijo compatible con el contrato del dispositivo."""
    duracion_segundos: float = 0.35
    frecuencia_tono_hz: float = 523.25
    amplitud: int = 6_000
    cantidad_muestras: int = round(FRECUENCIA_REQUERIDA_HZ * duracion_segundos)
    contenido: BytesIO = BytesIO()

    with wave.open(contenido, "wb") as archivo:
        archivo.setnchannels(CANALES_REQUERIDOS)
        archivo.setsampwidth(BITS_REQUERIDOS // 8)
        archivo.setframerate(FRECUENCIA_REQUERIDA_HZ)
        for indice in range(cantidad_muestras):
            angulo: float = 2 * math.pi * frecuencia_tono_hz * indice / FRECUENCIA_REQUERIDA_HZ
            muestra: int = round(amplitud * math.sin(angulo))
            archivo.writeframesraw(struct.pack("<h", muestra))

    return contenido.getvalue()
