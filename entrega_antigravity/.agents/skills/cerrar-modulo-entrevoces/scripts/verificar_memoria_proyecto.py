"""Verifica la presencia y coherencia básica de la memoria de EntreVoces."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


RUTAS_OBLIGATORIAS = (
    "AGENTS.md",
    "PROJECT_STATE.md",
    "documentacion/PLAN_DESARROLLO_MVP.md",
    "documentacion/DOCUMENTACION_TECNICA.md",
    "documentacion/REGISTRO_CAMBIOS.md",
)

EXTENSIONES_CODIGO = {
    ".c",
    ".cpp",
    ".dart",
    ".h",
    ".hpp",
    ".py",
    ".sql",
    ".ts",
    ".yaml",
    ".yml",
}

DIRECTORIOS_IGNORADOS = {
    ".agents",
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "documentacion",
}


@dataclass(frozen=True)
class ResultadoMemoria:
    """Representa la coherencia observable de la memoria del proyecto."""

    raiz: str
    valido: bool
    faltantes: list[str]
    errores: list[str]
    advertencias: list[str]


def busca_codigo_mas_reciente(raiz: Path) -> Path | None:
    """Busca el archivo de código más reciente fuera de rutas ignoradas."""

    candidatos: list[Path] = []
    for ruta in raiz.rglob("*"):
        if not ruta.is_file() or ruta.suffix.lower() not in EXTENSIONES_CODIGO:
            continue
        if any(parte in DIRECTORIOS_IGNORADOS for parte in ruta.parts):
            continue
        candidatos.append(ruta)
    if not candidatos:
        return None
    return max(candidatos, key=lambda elemento: elemento.stat().st_mtime)


def verifica_memoria(raiz: Path) -> ResultadoMemoria:
    """Comprueba archivos obligatorios, referencias obsoletas y actualidad básica."""

    faltantes = [
        ruta for ruta in RUTAS_OBLIGATORIAS if not (raiz / ruta).is_file()
    ]
    errores: list[str] = []
    advertencias: list[str] = []

    if faltantes:
        return ResultadoMemoria(
            raiz=str(raiz),
            valido=False,
            faltantes=faltantes,
            errores=[],
            advertencias=[],
        )

    estado = raiz / "PROJECT_STATE.md"
    contenido_estado = estado.read_text(encoding="utf-8")
    registro = raiz / "documentacion/REGISTRO_CAMBIOS.md"
    contenido_registro = registro.read_text(encoding="utf-8")

    if "Siguiente paso" not in contenido_estado:
        errores.append("PROJECT_STATE.md no declara el siguiente paso.")
    if "Última actualización" not in contenido_estado:
        errores.append("PROJECT_STATE.md no declara su última actualización.")
    if "outputs/" in contenido_estado or "outputs/" in contenido_registro:
        errores.append("La memoria conserva referencias obsoletas a outputs/.")

    codigo_reciente = busca_codigo_mas_reciente(raiz)
    if codigo_reciente is not None:
        fecha_codigo = codigo_reciente.stat().st_mtime
        if estado.stat().st_mtime < fecha_codigo:
            advertencias.append(
                "PROJECT_STATE.md es anterior al archivo de código más reciente: "
                f"{codigo_reciente.relative_to(raiz)}."
            )
        if registro.stat().st_mtime < fecha_codigo:
            advertencias.append(
                "REGISTRO_CAMBIOS.md es anterior al archivo de código más reciente: "
                f"{codigo_reciente.relative_to(raiz)}."
            )

    return ResultadoMemoria(
        raiz=str(raiz),
        valido=not errores and not faltantes,
        faltantes=faltantes,
        errores=errores,
        advertencias=advertencias,
    )


def crea_analizador() -> argparse.ArgumentParser:
    """Crea el analizador de argumentos del verificador."""

    analizador = argparse.ArgumentParser(
        description="Verifica la memoria documental de EntreVoces."
    )
    analizador.add_argument("raiz", type=Path, help="Raíz del proyecto.")
    analizador.add_argument("--json", action="store_true", dest="como_json")
    return analizador


def main() -> int:
    """Ejecuta la verificación y devuelve un código apto para automatización."""

    argumentos = crea_analizador().parse_args()
    raiz = argumentos.raiz.resolve()
    if not raiz.is_dir():
        print(f"La raíz no existe o no es un directorio: {raiz}", file=sys.stderr)
        return 2

    resultado = verifica_memoria(raiz)
    if argumentos.como_json:
        print(json.dumps(asdict(resultado), ensure_ascii=False, indent=2))
    else:
        print(f"Raíz: {resultado.raiz}")
        print(f"Válido: {'sí' if resultado.valido else 'no'}")
        for faltante in resultado.faltantes:
            print(f"FALTA: {faltante}")
        for error in resultado.errores:
            print(f"ERROR: {error}")
        for advertencia in resultado.advertencias:
            print(f"ADVERTENCIA: {advertencia}")
    return 0 if resultado.valido else 1


if __name__ == "__main__":
    raise SystemExit(main())

