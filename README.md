# Reglas Cursor — uso por proyecto y cuándo las aplica el agente
Este paquete contiene reglas en .cursor/rules/ (archivos .mdc con frontmatter). Cursor las carga solo en el workspace donde exista esa carpeta; no son globales del sistema salvo que copies o enlaces este árbol en cada proyecto.

---

## Cómo instalar en un proyecto
Copia la carpeta .cursor del repo a la raíz de tu otro repositorio (o enlázala / súbela como submódulo según tu flujo).
Abre ese proyecto en Cursor. Las reglas aparecerán en Settings → Rules junto al resto de reglas del proyecto.
Cómo decide el agente cuándo usar cada regla
En cada .mdc, el frontmatter controla el comportamiento:

## Configuración	Efecto
alwaysApply: true	El agente siempre incluye esa regla en el chat (estándares generales, naming, filosofía).
alwaysApply: false + description clara	Modo “Apply intelligently”: el agente elige incluir la regla cuando el contexto y la descripción encajan (ej. “Estándares PHP: strict_types, prepared statements”).
globs: **/*.tsx (o el patrón que definas)	La regla se considera cuando trabajas con archivos que coinciden con el patrón (ej. UI minimalista solo en .tsx / .css).
Por tanto: tú no “invocas” regla a regla a mano en cada mensaje; defines siempre, por archivo (globs) o por relevancia (description + alwaysApply: false).

## Recomendación para tu paquete “básico”
Siempre activas: filosofía del agente, naming, y cualquier norma que no quieras que se omita nunca.
Solo cuando el modelo lo juzgue relevante: stacks concretos (PHP, JS/TS) con alwaysApply: false y una description explícita (ej. “Aplica al editar archivos PHP del backend”).
Solo al tocar ciertos archivos: UI / estilos con globs acotados (**/*.tsx, **/*.css, etc.).
Así el agente mezcla reglas globales del paquete con las que añadas solo en ese repo (dominio, Strapi, etc.).

## Prioridad y conflictos
Si una regla del proyecto contradice una de este paquete, la convención habitual de Cursor es que las reglas del proyecto (equipo / repo) pueden prevalecer según orden de fusión; mantén las reglas de este repo genéricas y deja los detalles del stack en .cursor/rules del proyecto concreto.

## Buenas descripciones (para que el agente acierte)
Mala: “Cosas de código.”
Buena: “Convenciones PHP: declare(strict_types=1), namespace inicial, prepared statements, sin SQL interpolado.”
Cuanto más concreta sea la description, más fácil es que el agente active esa regla solo cuando toque ese tipo de trabajo.
