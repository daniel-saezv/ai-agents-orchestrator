#!/usr/bin/env python3
"""Pruebas del validador. Cubre el fallo a propósito y el caso bueno."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validar

RAIZ = Path(__file__).resolve().parent.parent


def _base(raiz: Path) -> None:
    (raiz / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    (raiz / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [0.1.0] - pendiente\n",
        encoding="utf-8",
    )
    skill = raiz / "skills" / "demo"
    skill.mkdir(parents=True)
    (skill / "nota.md").write_text("Nota.\n", encoding="utf-8")
    (skill / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Prueba.\n---\n\n"
        "# Demo\n\nVer [nota](nota.md) y [web](https://example.com).\n",
        encoding="utf-8",
    )


def _exige_fallo(raiz: Path, texto: str) -> None:
    errores = validar.validar(raiz)
    if not any(texto in error for error in errores):
        raise AssertionError(errores)


def test_arbol_valido() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        errores = validar.validar(raiz)
        if errores:
            raise AssertionError(errores)


def test_frontmatter_sin_name() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        skill = raiz / "skills" / "demo" / "SKILL.md"
        skill.write_text(
            "---\ndescription: Prueba.\n---\n\n# Demo\n",
            encoding="utf-8",
        )
        _exige_fallo(raiz, "falta name")


def test_name_distinto_de_la_carpeta() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        skill = raiz / "skills" / "demo" / "SKILL.md"
        texto = skill.read_text(encoding="utf-8").replace("name: demo", "name: otra")
        skill.write_text(texto, encoding="utf-8")
        _exige_fallo(raiz, "la carpeta es")


def test_enlace_roto() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        nota = raiz / "skills" / "demo" / "SKILL.md"
        texto = nota.read_text(encoding="utf-8").replace("nota.md", "no-existe.md")
        nota.write_text(texto, encoding="utf-8")
        _exige_fallo(raiz, "enlace roto")


def test_nombre_prohibido() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        reglas = raiz / "reglas"
        reglas.mkdir()
        (reglas / "mal.md").write_text(
            "Hola " + ("Grok" " Bot") + ".\n",
            encoding="utf-8",
        )
        _exige_fallo(raiz, "nombre prohibido")


def test_variants_no_es_un_nombre() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        nota = raiz / "skills" / "demo" / "nota.md"
        nota.write_text("Campo `variants` del catálogo.\n", encoding="utf-8")
        errores = validar.validar(raiz)
        if errores:
            raise AssertionError(errores)


def test_nombre_dentro_de_adaptadores() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        destino = raiz / "adaptadores"
        destino.mkdir()
        (destino / "nota.md").write_text(("Thr" "all") + "\n", encoding="utf-8")
        errores = validar.validar(raiz)
        if errores:
            raise AssertionError(errores)


def test_changelog_no_coincide() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        raiz = Path(carpeta)
        _base(raiz)
        (raiz / "VERSION").write_text("0.2.0\n", encoding="utf-8")
        _exige_fallo(raiz, "CHANGELOG.md abre con 0.1.0 y VERSION es 0.2.0")


def test_repo() -> None:
    errores = validar.validar(RAIZ)
    if errores:
        raise AssertionError(errores)


def main() -> int:
    pruebas = [valor for nombre, valor in globals().items() if nombre.startswith("test_")]
    fallos = 0
    for prueba in pruebas:
        try:
            prueba()
        except Exception as exc:
            fallos += 1
            print(f"FALLO {prueba.__name__}: {exc}")
        else:
            print(f"ok {prueba.__name__}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
