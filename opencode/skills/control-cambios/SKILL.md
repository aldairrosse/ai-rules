---
name: control-cambios
description: Genera textos breves para control de cambios en tono de Product Manager. Usar cuando el usuario pida descripción breve, origen, justificación o afectación a servicios de un cambio, especialmente si menciona control de cambios, módulos en productivo, plans, changes, Markdown o contexto de git.
---

# Control Cambios

## Instrucciones

Genera 4 apartados:

- DESCRIPCIÓN BREVE DEL CAMBIO
- ORIGEN DEL CAMBIO
- JUSTIFICACIÓN
- AFECTACIÓN A SERVICIOS

Usa solo contexto disponible y relevante:

- Archivos de `plans`, `changes` o `.md`
- `git status`
- `git log`
- Archivos o texto que el usuario entregue

Mantén tono breve, claro y apto para Product Manager. Un párrafo por apartado.

No inventes impacto técnico. Si no hay evidencia, usa alcance conservador.

Entrega cada apartado en un bloque copiable separado. El título va fuera del bloque, nunca dentro.

## Formato

````markdown
DESCRIPCIÓN BREVE DEL CAMBIO

```text
[Párrafo breve sin título dentro del bloque]
```

ORIGEN DEL CAMBIO

```text
[Párrafo breve sin título dentro del bloque]
```

JUSTIFICACIÓN

```text
[Párrafo breve sin título dentro del bloque]
```

AFECTACIÓN A SERVICIOS

```text
[Párrafo breve sin título dentro del bloque]
```
````

## Criterios

- Sin listas dentro de los bloques.
- Sin lenguaje técnico innecesario.
- Sin promesas de valor no evidenciadas.
- Sin mencionar bases de datos, correo, FTP u otros servicios como afectados salvo evidencia.
- Sin mencionar referencias de archivos o código.
