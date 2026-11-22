#!/usr/bin/env python3
"""Comprueba frontmatter, enlaces relativos, nombres prohibidos y versión."""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Cadenas partidas: el nombre seguido no puede aparecer fuera de adaptadores/.
PROHIBIDOS = (
    "Thr" "all",
    "Var" "ian",
    "Grok" " Bot",
    "Gamu" "sino",
)

SEMVER = re.compile(r"\d+\.\d+\.\d+")
ENLACE = re.compile(r"\[[^\]]*\]\(\s*([^)]+?)\s*\)")
ENTRADA_CAMBIO = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.M)
SALTAR = {".git", "__pycache__"}


def validar(raiz: Path) -> list[str]:
    return _version(raiz) + _skills(raiz) + _enlaces(raiz) + _nombres(raiz)


def _version(raiz: Path) -> list[str]:
    version_path = raiz / "VERSION"
    cambio_path = raiz / "CHANGELOG.md"
    if not version_path.is_file():
        return ["falta VERSION"]
    version = version_path.read_text(encoding="utf-8").strip()
    if SEMVER.fullmatch(version) is None:
        return [f"VERSION no es SemVer: {version!r}"]
    if not cambio_path.is_file():
        return ["falta CHANGELOG.md"]
    encontradas = ENTRADA_CAMBIO.findall(cambio_path.read_text(encoding="utf-8"))
    if not encontradas:
        return ["CHANGELOG.md no tiene una entrada ## [x.y.z]"]
    if encontradas[0] != version:
        return [f"CHANGELOG.md abre con {encontradas[0]} y VERSION es {version}"]
    return []


def _skills(raiz: Path) -> list[str]:
    encontrados = [
        path
        for path in raiz.rglob("SKILL.md")
        if _visible(path.relative_to(raiz))
    ]
    if not encontrados:
        return ["no hay ningún SKILL.md"]
    errores: list[str] = []
    for path in encontrados:
        errores += _un_skill(raiz, path)
    return errores


def _un_skill(raiz: Path, path: Path) -> list[str]:
    rel = path.relative_to(raiz).as_posix()
    texto = _texto(path)
    if texto is None:
        return [f"{rel}: no es UTF-8"]
    datos, error = _frontmatter(texto)
    if error:
        return [f"{rel}: {error}"]
    errores: list[str] = []
    nombre = datos.get("name", "").strip()
    descripcion = datos.get("description", "").strip()
    if not nombre:
        errores.append(f"{rel}: falta name")
    if not descripcion:
        errores.append(f"{rel}: falta description")
    if nombre and nombre != path.parent.name:
        errores.append(f"{rel}: name es {nombre!r} y la carpeta es {path.parent.name!r}")
    return errores


def _frontmatter(texto: str) -> tuple[dict[str, str] | None, str | None]:
    if not texto.startswith("---\n"):
        return None, "el frontmatter no abre con ---"
    fin = texto.find("\n---\n", 3)
    if fin == -1:
        return None, "el frontmatter no cierra"
    datos: dict[str, str] = {}
    for numero, linea in enumerate(texto[4:fin].splitlines(), start=2):
        if not linea.strip():
            continue
        if ":" not in linea:
            return None, f"línea {numero} del frontmatter sin clave"
        clave, valor = linea.split(":", 1)
        clave = clave.strip()
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in {"'", '"'}:
            valor = valor[1:-1].strip()
        if not clave:
            return None, f"línea {numero} con clave vacía"
        if clave in datos:
            return None, f"clave duplicada: {clave}"
        datos[clave] = valor
    return datos, None


def _enlaces(raiz: Path) -> list[str]:
    errores: list[str] = []
    raiz_res = raiz.resolve()
    for path in raiz.rglob("*.md"):
        rel = path.relative_to(raiz)
        if not _visible(rel):
            continue
        texto = _texto(path)
        if texto is None:
            errores.append(f"{rel.as_posix()}: no es UTF-8")
            continue
        visible = re.sub(r"```.*?```", "", texto, flags=re.S)
        for match in ENLACE.finditer(visible):
            ruta = _ruta_enlace(match.group(1))
            if ruta is None:
                continue
            destino = (path.parent / ruta).resolve()
            try:
                destino.relative_to(raiz_res)
            except ValueError:
                errores.append(f"{rel.as_posix()}: enlace fuera del repo ({ruta})")
                continue
            if not destino.exists():
                errores.append(f"{rel.as_posix()}: enlace roto ({ruta})")
    return errores


def _ruta_enlace(crudo: str) -> str | None:
    trozo = crudo.strip()
    if trozo.startswith("<") and ">" in trozo:
        trozo = trozo[1 : trozo.index(">")]
    if not trozo:
        return None
    trozo = trozo.split()[0]
    if trozo.startswith("#") or "://" in trozo or trozo.startswith("mailto:"):
        return None
    ruta = trozo.split("#", 1)[0].split("?", 1)[0]
    return ruta or None


def _nombres(raiz: Path) -> list[str]:
    errores: list[str] = []
    patrones = [_patron(nombre) for nombre in PROHIBIDOS]
    for path in raiz.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(raiz)
        if not rel.parts or rel.parts[0] in {".git", "adaptadores"} or not _visible(rel):
            continue
        texto = _texto(path)
        if texto is None:
            continue
        for nombre, patron in zip(PROHIBIDOS, patrones):
            if patron.search(texto):
                errores.append(f"{rel.as_posix()}: nombre prohibido ({nombre})")
    return errores


def _patron(nombre: str) -> re.Pattern[str]:
    cuerpo = r"\s+".join(re.escape(parte) for parte in nombre.split())
    return re.compile(rf"\b{cuerpo}\b", re.IGNORECASE)


def _visible(rel: Path) -> bool:
    return not any(parte in SALTAR for parte in rel.parts)


def _texto(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def main() -> int:
    errores = validar(RAIZ)
    if errores:
        for error in errores:
            print(error)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
