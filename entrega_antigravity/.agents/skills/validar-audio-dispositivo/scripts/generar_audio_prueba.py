"""Genera un WAV controlado compatible con el MVP de EntreVoces."""

from __future__ import annotations

import argparse
import math
import struct
import wave
from pathlib import Path


FRECUENCIA_MUESTREO_HZ = 16_000
AMPLITUD_MAXIMA = 32_767


def genera_tono(
    ruta: Path,
    duracion_segundos: float,
    frecuencia_tono_hz: float,
    amplitud: float,
) -> None:
    """Genera un tono mono de 16 bits y 16 kHz sin sobrescribir archivos."""

    if ruta.exists():
        raise FileExistsError(f"El archivo ya existe: {ruta}")
    if duracion_segundos <= 0:
        raise ValueError("La duración debe ser mayor que cero.")
    if frecuencia_tono_hz <= 0:
        raise ValueError("La frecuencia del tono debe ser mayor que cero.")
    if not 0 < amplitud <= 1:
        raise ValueError("La amplitud debe estar entre 0 y 1.")

    ruta.parent.mkdir(parents=True, exist_ok=True)
    cantidad_muestras = round(FRECUENCIA_MUESTREO_HZ * duracion_segundos)
    escala = round(AMPLITUD_MAXIMA * amplitud)

    with wave.open(str(ruta), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(FRECUENCIA_MUESTREO_HZ)
        for indice in range(cantidad_muestras):
            valor = round(
                escala
                * math.sin(
                    2 * math.pi * frecuencia_tono_hz * indice / FRECUENCIA_MUESTREO_HZ
                )
            )
            audio.writeframesraw(struct.pack("<h", valor))


def crea_analizador() -> argparse.ArgumentParser:
    """Crea el analizador de argumentos del generador."""

    analizador = argparse.ArgumentParser(
        description="Genera un WAV mono PCM de 16 kHz y 16 bits."
    )
    analizador.add_argument("ruta", type=Path, help="Ruta WAV de salida.")
    analizador.add_argument("--duracion", type=float, default=1.0)
    analizador.add_argument("--frecuencia-tono", type=float, default=440.0)
    analizador.add_argument("--amplitud", type=float, default=0.2)
    return analizador


def main() -> int:
    """Genera la muestra controlada solicitada."""

    argumentos = crea_analizador().parse_args()
    try:
        genera_tono(
            argumentos.ruta.resolve(),
            argumentos.duracion,
            argumentos.frecuencia_tono,
            argumentos.amplitud,
        )
    except (FileExistsError, OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"Audio generado: {argumentos.ruta.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

