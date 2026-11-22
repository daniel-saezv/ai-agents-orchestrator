# Cursor: elegir y comprobar el modelo

Hechos para consultar. Valen en cualquier repositorio. Si un campo no está aquí, no lo inventes: abre el enlace. No copies ids de modelo a esta skill: el catálogo cambia.

Reglas de equipo: [equipo.md](../../../reglas/equipo.md).

## Documentación

- Catálogo de ids y parámetros del cloud agent: [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints), acción List Models (`GET /v1/models`).
- Qué está incluido y qué descuento hay en este momento: [Models & Pricing](https://cursor.com/docs/models-and-pricing) (pool de modelos de Cursor frente a terceros a precio de API).
- Cómo pasar el modelo al crear el agente: el mismo [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints), `POST /v1/agents` (`model.id`, `model.params`).
- Modelo por defecto si omites `model`: [Cloud Agents settings](https://cursor.com/docs/cloud-agent/settings).

## Cómo consultar el catálogo

Antes de lanzar, pide `GET /v1/models`. Usa un `id` de esa respuesta y solo los `parameters` / `variants` que liste para ese modelo.

En [Models & Pricing](https://cursor.com/docs/models-and-pricing), mira el pool incluido, lo que se cobra aparte y los descuentos del momento. Esta skill no enumera esa lista. No copies la tabla aquí.

La familia que puede ir en Cursor está en las reglas de equipo. El id concreto sale del catálogo de ahora.

## Cómo elegir

Al lanzar el cloud agent, selecciona el modelo. En la API, pásalo en el cuerpo de `POST /v1/agents`:

- `model.id`: un id que devuelva `GET /v1/models` ahora.
- `model.params`: lista de `{ "id", "value" }`. Pasa `fast=false` siempre que el modelo admita ese parámetro. Nunca `true`. El resto de parámetros, solo los que `GET /v1/models` liste para ese id.

Si omites `model`, Cursor resuelve el modelo por defecto del usuario, luego el del equipo, luego el del sistema. Esta skill exige pasarlo siempre.

## Cómo comprobar

El modelo pedido no basta. Lee el que muestra el agente o la ejecución: el selector o la ficha del run, y el MCP Cursor Cloud (`run-info`) en la ejecución actual.

`GET /v1/agents/{id}` y `GET /v1/agents/{id}/runs/{runId}` no documentan un campo de modelo. No lo inventes.
