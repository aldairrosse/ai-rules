# Reglas Cursor — uso por proyecto y cuándo las aplica el agente

Paquete de reglas en **`.cursor/rules/`** (archivos `.mdc` con frontmatter). Cursor solo las carga en el workspace donde exista esa ruta; un `remote` en Git no las aplica en otros repos hasta que copies o enlaces esa carpeta allí.

---

## Estructura básica

```text
ai-rules/
├── README.md
└── .cursor/rules/
    ├── agent-philosophy-workflow.mdc
    ├── naming-conventions.mdc
    ├── javascript-typescript-standards.mdc
    ├── php-standards.mdc
    └── ui-minimalist.mdc
```

---

## Reglas incluidas

| Archivo | Contenido (resumen) | Activación |
|--------|----------------------|------------|
| `agent-philosophy-workflow.mdc` | Clean Code, KISS/DRY, Git, comentarios, protocolo del agente y límites de alcance | Siempre (`alwaysApply: true`) |
| `naming-conventions.mdc` | Estilos de nombres (código y BD) | Siempre |
| `javascript-typescript-standards.mdc` | JS/TS: npm, async/await, DOM | Por globs `*.{ts,tsx,js,jsx,mjs,cjs}` |
| `php-standards.mdc` | PHP: `strict_types`, Composer, SQL preparado, namespaces | Por globs `*.php` |
| `ui-minimalist.mdc` | UI minimalista: tipografía, bordes, sombras, animación | Por globs `*.{tsx,jsx,css,scss}` |

---

## Cómo instalar en un proyecto

Copia la carpeta `.cursor` del repo a la raíz de tu otro repositorio (o enlázala / úsala como submódulo). Abre ese proyecto en Cursor: **Settings → Rules** debería listar estas reglas junto a las del repo.

---

## Cómo decide el agente cuándo usar cada regla

En cada `.mdc`, el frontmatter controla el comportamiento:

| Configuración | Efecto |
|---------------|--------|
| `alwaysApply: true` | El agente siempre incluye la regla (p. ej. filosofía y naming). |
| `alwaysApply: false` + `description` clara | El agente la incluye cuando el contexto encaja con la descripción. |
| `globs: **/*.tsx` (u otro patrón) | Se considera al trabajar en archivos que coincidan (p. ej. UI solo en `.tsx` / `.css`). |

No hace falta invocar reglas a mano: defines siempre-on, por relevancia o por tipo de archivo.

---

## Recomendación para el paquete “básico”

- **Siempre:** filosofía del agente y naming (y lo que no quieras que se omita nunca).
- **Bajo demanda:** stacks concretos (PHP, JS/TS) con `alwaysApply: false` y `description` explícita.
- **Por archivos:** UI / estilos con globs acotados.

Así puedes mezclar este paquete con reglas solo de ese repo (dominio, Strapi, etc.).

---

## Prioridad y conflictos

Si una regla del proyecto contradice una de este paquete, suele prevalecer la del proyecto según cómo Cursor fusione el contexto. Mantén aquí reglas genéricas y el detalle del stack en `.cursor/rules` del repo concreto.

---

## Buenas descripciones (para que el agente acierte)

- Mala: “Cosas de código.”
- Buena: “Convenciones PHP: `declare(strict_types=1)`, namespace inicial, prepared statements, sin SQL interpolado.”

Cuanto más concreta sea la `description`, más fácil es que la regla condicional se active solo cuando toque ese trabajo.
