---
name: elegir-modelo
description: Elige y comprueba el modelo de un agente en la nube. Pasa el modelo de forma explícita y justifica plataforma y modelo en el encargo y en el informe.
---

# Elegir modelo

Usa esta skill al lanzar un agente en la nube. Vale en cualquier repositorio.

Las reglas de equipo están en [reglas/equipo.md](../../reglas/equipo.md). Los detalles de cada plataforma (dónde consultar el catálogo, cómo pasar el modelo, cómo comprobarlo) están en [referencias/cursor.md](referencias/cursor.md) y [referencias/copilot.md](referencias/copilot.md). No los copies al repositorio que lanza al agente.

## Qué hacer

1. **Elige plataforma y modelo juntos.** Mira la tarea. Consulta el catálogo vigente y los descuentos del momento, no una lista memorizada. Aplica las [reglas de equipo](../../reglas/equipo.md). Justifica ambos en el encargo y en el informe.
2. **Pasa el modelo de forma explícita.** Nunca dejes el de por defecto. Sigue la referencia de la plataforma: id, parámetros y el canal con el que lanzas.
3. **Comprueba el modelo que se resolvió realmente.** No asumas que el id pedido es el usado. Lee el dato que documenta la referencia.
4. **Aplica las reglas de equipo.** Si el modelo resuelto no coincide con lo justificado, para y relanza.

## Qué no hacer

- No dejes el modelo por defecto de la cuenta, el equipo o el sistema.
- No copies a esta skill ni al repositorio que lanza al agente una lista de ids de modelo. Cambian.
- No fijes una plataforma para todas las tareas. Se elige en cada una.
