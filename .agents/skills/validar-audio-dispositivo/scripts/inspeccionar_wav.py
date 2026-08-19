"""Inspecciona un archivo WAV y comprueba el contrato de EntreVoces."""

from __future__ import annotations

import argparse
import json
import sys
import wave
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResultadoAudio:
    """Representa el resultado verificable de una inspección WAV."""

    ruta: str
    valido: bool
    canales: int | None
    frecuencia_hz: int | None
    bits_por_muestra: int | None
    fotogramas: int | None
    duracion_segundos: float | None
    compresion: str | None
    errores: list[str]
    advertencias: list[str]


def inspecciona_wav(ruta: Path, duracion_maxima: float) -> ResultadoAudio:
    """Inspecciona el WAV y devuelve sus incumplimientos sin modificarlo."""

    errores: list[str] = []
    advertencias: list[str] = []

    if not ruta.is_file():
        return ResultadoAudio(
            ruta=str(ruta),
            valido=False,
            canales=None,
            frecuencia_hz=None,
            bits_por_muestra=None,
            fotogramas=None,
            duracion_segundos=None,
            compresion=None,
            errores=["El archivo no existe o no es un archivo regular."],
            advertencias=[],
        )

    if ruta.suffix.lower() != ".wav":
        advertencias.append("La extensión no es .wav, aunque se intentará leer el contenido.")

    try:
        with wave.open(str(ruta), "rb") as audio:
            canales = audio.getnchannels()
            frecuencia_hz = audio.getframerate()
            bytes_por_muestra = audio.getsampwidth()
            bits_por_muestra = bytes_por_muestra * 8
            fotogramas = audio.getnframes()
            compresion = audio.getcomptype()
            duracion_segundos = (
                fotogramas / frecuencia_hz if frecuencia_hz > 0 else 0.0
            )
    except (OSError, EOFError, wave.Error) as error:
        return ResultadoAudio(
            ruta=str(ruta),
            valido=False,
            canales=None,
            frecuencia_hz=None,
            bits_por_muestra=None,
            fotogramas=None,
            duracion_segundos=None,
            compresion=None,
            errores=[f"No se pudo interpretar el archivo como WAV: {error}"],
            advertencias=advertencias,
        )

    if compresion != "NONE":
        errores.append(f"La compresión debe ser PCM sin compresión; se obtuvo {compresion}.")
    if canales != 1:
        errores.append(f"El audio debe tener un canal; se obtuvieron {canales}.")
    if frecuencia_hz != 16_000:
        errores.append(
            f"La frecuencia debe ser 16000 Hz; se obtuvieron {frecuencia_hz} Hz."
        )
    if bits_por_muestra != 16:
        errores.append(
            f"La profundidad debe ser 16 bits; se obtuvieron {bits_por_muestra} bits."
        )
    if fotogramas <= 0 or duracion_segundos <= 0:
        errores.append("El audio no contiene muestras reproducibles.")
    if duracion_segundos > duracion_maxima:
        errores.append(
            "La duración supera el máximo configurado de "
            f"{duracion_maxima:.3f} segundos."
        )

    return ResultadoAudio(
        ruta=str(ruta),
        valido=not errores,
        canales=canales,
        frecuencia_hz=frecuencia_hz,
        bits_por_muestra=bits_por_muestra,
        fotogramas=fotogramas,
        duracion_segundos=round(duracion_segundos, 6),
        compresion=compresion,
        errores=errores,
        advertencias=advertencias,
    )


def crea_analizador() -> argparse.ArgumentParser:
    """Crea el analizador de argumentos del inspector."""

    analizador = argparse.ArgumentParser(
        description="Comprueba el contrato WAV del MVP de EntreVoces."
    )
    analizador.add_argument("ruta", type=Path, help="Ruta del archivo WAV.")
    analizador.add_argument(
        "--duracion-maxima",
        type=float,
        default=60.0,
        help="Duración máxima permitida en segundos.",
    )
    analizador.add_argument(
        "--json",
        action="store_true",
        dest="como_json",
        help="Emite el resultado como JSON.",
    )
    return analizador


def main() -> int:
    """Ejecuta la inspección y devuelve un código apto para automatización."""

    argumentos = crea_analizador().parse_args()
    if argumentos.duracion_maxima <= 0:
        print("La duración máxima debe ser mayor que cero.", file=sys.stderr)
        return 2

    resultado = inspecciona_wav(argumentos.ruta.resolve(), argumentos.duracion_maxima)
    if argumentos.como_json:
        print(json.dumps(asdict(resultado), ensure_ascii=False, indent=2))
    else:
        print(f"Archivo: {resultado.ruta}")
        print(f"Válido: {'sí' if resultado.valido else 'no'}")
        print(f"Canales: {resultado.canales}")
        print(f"Frecuencia: {resultado.frecuencia_hz} Hz")
        print(f"Profundidad: {resultado.bits_por_muestra} bits")
        print(f"Duración: {resultado.duracion_segundos} s")
        for error in resultado.errores:
            print(f"ERROR: {error}")
        for advertencia in resultado.advertencias:
            print(f"ADVERTENCIA: {advertencia}")

    if resultado.canales is None:
        return 2
    return 0 if resultado.valido else 1


if __name__ == "__main__":
    raise SystemExit(main())

