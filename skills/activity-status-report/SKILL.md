---
name: activity-status-report
description: Genera reportes de avance en texto plano (correo), siempre en un bloque de código del chat copiable, no suelto en el mensaje. Un solo emoji antes de la palabra de estatus, sin punto y coma, salto en blanco entre tareas. Títulos iniciando con verbo infinitivo; descripciones breves, sin referencias de código y con el mínimo de conceptos técnicos. Pendientes, stoppers y dependencias solo si aplican. Usa cuando el usuario pide reporte de estatus, actividad, progreso o "status report".
---

# Reporte de estatus de actividades

## Antes de redactar (solo contexto; no volcar esto al reporte)

1. Revisar en el repo lo que haya de plan o seguimiento y la conversación o terminal si aporta cierre.
2. Preguntar al usuario si hay dudas sobre qué incluir o cómo redactar si la actividad no está clara.

## En el cuerpo del reporte: qué no incluir

- Rutas, nombres de archivo, módulos por ruta, variables, hooks, componentes con nombre de archivo.
- Sí, muy breve: aspectos técnicos genéricos: lógica, reglas de negocio, endpoints, tablas, módulos, capa de API, controlador, integración, plantilla, validaciones.

## Estructura por actividad

- Descripción en viñetas o frases breves: qué se hizo. **Sin ninguna referencia de código** (archivos, rutas, variables, componentes) y con el **mínimo de conceptos técnicos** (API, SQL, Script, Cron, endpoint, tabla, etc.): usarlos solo cuando sean imprescindibles para entender el avance; preferir lenguaje de negocio.
- Agrupar por fase o proyecto si aplica.
- Cada título **inicia con un verbo en infinitivo** (p. ej. "Implementar webhooks para Mobofácil", no "Implementación de webhooks"). Títulos claros y concisos, sin jerga ni siglas internas. Evitar nombres de archivo, rutas, variables, componentes o módulos.

## Un solo estatus por ítem

- **Un solo emoji** en toda la línea de encabezado, colocado **justo antes** de la palabra del estado (p. ej. `→ 🟡 En proceso` o `→ ✅ Completado`). No añadir otros emojis en títulos, cuerpo ni secciones opcionales.
- Texto del estatus: Completado, En proceso, Bloqueado (o frase corta equivalente).

## Secciones opcionales (solo si aplican)

- PENDIENTES, STOPPERS, DEPENDENCIAS (con **¿Contacto iniciado?: Sí|No** si hay dependencia).
- Si no aplica sección de PENDIENTES, STOPPERS o DEPENDENCIAS: omitir toda la sección (Nunca incluir "Ninguno" / "Ninguna").

## Formato de salida (obligatorio)

**Texto plano** dentro del reporte, para correo. **Sin markdown** en el cuerpo (sin `#`, negritas, listas md, etc. dentro del reporte).

**Cómo entregar la respuesta en el chat:** el reporte completo **siempre** en **un solo** bloque de código (triple backtick) para copiar con un clic. **No** repartir el contenido del reporte como párrafos o viñetas sueltas fuera de ese bloque. Texto de ayuda previo o posterior, si hace falta, en una o dos líneas como mucho, separado del bloque.

**Línea de encabezado de cada actividad:**

- Formato: `• [Título] → [emoji][Estatus]` (el emoji pega a la primera palabra del estatus, sin puntuación extra al final de la línea).
- Tras esa línea: el texto de descripción (y bloques opcionales si aplica).
- Con **más de una tarea**: **línea en blanco** entre un bloque de tarea y el **siguiente** `• ...` (después de lo que cierre el bloque anterior, antes de la viñeta nueva).
- **No** usar el carácter `;` en el reporte (ni al final de línea ni en el cuerpo).

Plantilla (solo bloques con contenido real):

```
• [Título] → [emoji][Completado | En proceso | Bloqueado]
[Qué se hizo, claro y breve]

PENDIENTES:
- …

STOPPERS:
- …

DEPENDENCIAS:
- [equipo/sistema]  ¿Contacto iniciado?: Sí|No
```

## Ejemplos

```
• Implementar webhooks para Mobofácil → 🟡 En proceso
Las notificaciones de pago (aprobado o rechazado) ya llegan automáticamente y actualizan el pedido sin intervención manual.
PENDIENTES:
- Validar con el equipo de Nuovo
DEPENDENCIAS:
- Nuovo  ¿Contacto iniciado?: Sí
```

```
• Traducir correos en VTEX → 🟡 En proceso
Dos correos principales pasados a español: Orden cancelada, Orden realizada.
PENDIENTES:
- Revisar otros correos del Centro de Mensajes no traducidos
```

(Dos tareas: línea en blanco entre el cierre de la primera y la viñeta de la segunda.)

```
• Primera tarea de ejemplo → ✅ Completado
Cuerpo de la primera tarea. Sin secciones opcionales al final

• Segunda tarea de ejemplo → 🟡 En proceso
Cuerpo de la segunda. Aquí empieza tras el salto de línea
```

## No hacer

- Exponer el cuerpo del reporte directamente en el cuerpo del mensaje: debe ir dentro del bloque copiable.
- Más de un emoji por tarea, o emojis fuera de la posición fija antes del estatus.
- Citar archivos, carpetas, variables o identificadores de código.
- Abusar de tecnicismos (API, SQL, Script, Cron, endpoint): solo si son imprescindibles para entender el avance.
- Titulos que no empiecen con verbo en infinitivo.
- Rellenar secciones vacías con "Ninguno".
- Inventar hechos: sin dato, preguntar o "Por confirmar: …" bajo PENDIENTES.
- Juntar mas de dos tareas: tiene que mediar línea en blanco en el cierre de una y en la viñeta de la otra.
- Usar `;` en ninguna parte del texto generado.