# ai-agents-orchestrator

Fuente de verdad de las reglas para quien lanza agentes de código en la nube. Agnóstica de la plataforma. Versionada con SemVer.

## Para quién es

Para el orquestador que elige plataforma y modelo y redacta el encargo. También para un agente que tenga que aplicar esas reglas.

## Qué contiene

- [AGENTS.md](AGENTS.md): ruta de entrada.
- [reglas/equipo.md](reglas/equipo.md): reglas de equipo.
- [reglas/plataformas.md](reglas/plataformas.md): Cursor y GitHub Copilot.
- [skills/elegir-modelo/SKILL.md](skills/elegir-modelo/SKILL.md): skill para elegir y comprobar el modelo.

## Cómo se usa

Fija un tag. No sigas `main`.

Desde otro repositorio, enlaza la entrada en ese tag. No copies el texto.

```text
https://github.com/daniel-saezv/ai-agents-orchestrator/blob/v0.1.0/AGENTS.md
```

Desde un agente, lee ese archivo en el tag fijado y aplica lo que enlaza. La misma revisión en bruto:

```text
https://raw.githubusercontent.com/daniel-saezv/ai-agents-orchestrator/v0.1.0/AGENTS.md
```

El tag `v0.1.0` todavía no existe. Se crea sobre `main` después del merge. Hasta entonces no hay revisión que fijar.

## Cómo se versiona

La versión declarada está en [VERSION](VERSION). El historial está en [CHANGELOG.md](CHANGELOG.md).

- `VERSION` lleva `X.Y.Z`, sin `v`.
- El tag `vX.Y.Z` apunta al commit de `main` que publica esa versión.
- La fecha de `0.1.0` queda pendiente hasta ese tag.
- MAJOR rompe una regla que ya se aplica. MINOR añade una regla compatible. PATCH aclara sin cambiar la regla.

Quien consume las reglas fija el tag. Un cambio de reglas es una versión nueva.

## Ruta de entrada

[AGENTS.md](AGENTS.md)

## Comprobar en local

No hay instalación ni build.

```bash
python3 scripts/validar.py
python3 scripts/test_validar.py
```
