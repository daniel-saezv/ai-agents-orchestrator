# Entrada

Fuente de verdad de las reglas para quien lanza agentes de código en la nube. Agnóstica de la plataforma. Versionada con SemVer.

Este archivo es la ruta de entrada. Fija un tag y lee esa revisión. No sigas `main`.

## Qué aplicar

1. [reglas/equipo.md](reglas/equipo.md)
2. [reglas/plataformas.md](reglas/plataformas.md)
3. [skills/elegir-modelo/SKILL.md](skills/elegir-modelo/SKILL.md)

No copies estas reglas a otro repositorio. Enlaza el tag.

## Este repositorio

Texto y un validador en Python 3 de la biblioteca estándar. Sin dependencias y sin secretos.

### Estructura

- `AGENTS.md`: entrada.
- `reglas/`: equipo y plataformas.
- `skills/elegir-modelo/`: skill y referencias de Cursor y de Copilot.
- `scripts/validar.py`: comprueba el contenido.
- `scripts/test_validar.py`: pruebas del validador.
- `VERSION` y `CHANGELOG.md`: versión declarada.
- `.github/workflows/validar.yml`: CI.

### Comandos

No hay instalación, build ni arranque.

```bash
python3 scripts/validar.py
python3 scripts/test_validar.py
```

Verificado con Python 3.12.3.

### Práctica

La obligación está en `reglas/equipo.md`. La skill dice cómo cumplirla. El id de un modelo se consulta en el catálogo del momento. El validador no instala nada: el workflow solo hace checkout y corre Python.

### CI/CD

El workflow `Validar` corre en cada pull request y en cada push a `main`. Ejecuta el validador y sus pruebas. Es el check obligatorio.

El validador comprueba cuatro cosas: el frontmatter de cada `SKILL.md` (`name`, `description` y `name` igual al nombre de la carpeta), los enlaces relativos, los nombres prohibidos fuera de `adaptadores/` y que la primera entrada de `CHANGELOG.md` sea la versión de `VERSION`.

No hace falta ningún secreto.

El repositorio no se despliega. La publicación es el tag `vX.Y.Z` sobre `main`, después del merge. Quien consume las reglas fija ese tag. No hay paquete en un registro.
