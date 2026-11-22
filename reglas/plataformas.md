# Plataformas de agentes

Sirve en cualquier repositorio. No sustituye la documentación oficial.

El modelo se elige con la skill [elegir-modelo](../skills/elegir-modelo/SKILL.md). Las obligaciones están en [equipo.md](equipo.md).

## Cursor

El orquestador lanza el agente desde Cursor, sobre la URL del repositorio.

El agente crea una rama y abre la PR.

## GitHub Copilot

Se lanza asignando una issue a Copilot.

El login correcto es `copilot-swe-agent[bot]`. Con `Copilot` o `copilot-swe-agent`, la API responde 422. El mensaje es *Validation Failed (assignees: invalid)*.

La asignación vale por cualquiera de estas vías:

- `POST /repos/{owner}/{repo}/issues` con `assignees`
- `POST /repos/{owner}/{repo}/issues/{n}/assignees`
- `PATCH /repos/{owner}/{repo}/issues/{n}`

Se puede enviar `agent_assignment` con `target_repo`, `base_branch`, `custom_instructions`, `custom_agent` y `model`. Documentación: [Use Copilot cloud agent via the API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api).

Hace falta un token de usuario. Vale un PAT, un token OAuth o un token user-to-server de una GitHub App. No vale el token de instalación de una GitHub App.

Un PAT fine-grained necesita Metadata en lectura. También Actions, Contents, Issues y Pull requests en lectura y escritura. Un PAT classic necesita el ámbito `repo`.

La conexión de GitHub de Cursor es un token user-to-server. Cumple esos requisitos.

Para ver si Copilot se puede asignar en un repositorio, consulta en GraphQL `suggestedActors(capabilities: [CAN_BE_ASSIGNED])`. Tiene que aparecer `copilot-swe-agent`.

La PR queda con autor de quien asignó la issue. Copilot es coautor de los commits. La PR se abre en borrador.

El token no se imprime. No se escribe en archivos ni en logs.

Los workflows de las ramas de Copilot siguen la regla "Approve and run" de [equipo.md](equipo.md).

## Copilot: elegir y comprobar el modelo

Sigue la skill [elegir-modelo](../skills/elegir-modelo/SKILL.md).

Asigna la issue a `copilot-swe-agent[bot]`. Pasa `agent_assignment.model`. Sin `model`, Copilot usa Auto.

Un modelo que no está disponible no falla el HTTP. La issue se crea con 201. Copilot comenta que el modelo no está disponible. No abre sesión ni PR.

Revisa los comentarios de la issue después de asignar. El id resuelto está en el log del workflow **Running Copilot cloud agent**, en `resolved=`.

## Configuración que solo puede hacer el dueño del repo

Hay ajustes que piden `pages=write` o `administration=write`. La conexión de GitHub que usa Cursor no llega a eso: limita `pages` y `administration` a lectura.

Esos ajustes los hace el dueño del repo, a mano, una vez por repositorio. El orquestador no los inventa ni los salta.
