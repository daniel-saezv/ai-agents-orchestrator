# Reglas de equipo

Las cumple el orquestador. También un agente que lance otros agentes.

El procedimiento para elegir y comprobar el modelo está en la skill [elegir-modelo](../skills/elegir-modelo/SKILL.md). Las plataformas están en [plataformas.md](plataformas.md).

1. `fast=false` siempre. En Cursor, si el modelo admite el parámetro `fast`, el valor es `false`.
2. En Cursor solo Grok o Composer. El resto de modelos (Claude, GPT, Gemini, MAI Code…) van por Copilot.
3. Nada de listas fijas de modelos verificados. Antes de elegir, se consultan el catálogo actual y los descuentos del momento en Cursor y en Copilot. Los modelos entran y salen. Los descuentos cambian. El id se toma de ese catálogo.
4. En Copilot, un id de modelo no válido devuelve 201. Copilot lo rechaza en un comentario de la issue. Hay que confirmar en la issue y en el log el modelo resuelto.
5. En cada tarea se eligen plataforma y modelo. Se justifican en el encargo y en el informe.
6. Los workflows de las ramas de Copilot necesitan "Approve and run" antes de ejecutarse.
7. Los merges solo con la aprobación explícita del dueño del repo.
8. Señal de fin de Copilot: pendiente. El contenido llegará cuando termine el piloto. Hasta entonces esta regla no define ninguna señal.
