[[css/scss]] [[css/tailwindcss]] [[Optimizing performance]] [[React build]]

# React style inside component

> CSS colocated with JSX — CSS Modules, styled-components, **`styled-jsx` (Next.js)** — scope styles to component without global leaks — **CSS-in-JS tradeoffs**.

---

## Mental model

Options for component-local styling:

```txt
CSS Modules (*.module.css)   → build-time scoped class names (Vite default)
Tailwind utility classes      → [[css/tailwindcss]] in className
styled-jsx                    → <style jsx> injected per component (Next)
CSS-in-JS runtime             → styled-components (runtime cost)
Inline style={{}}             → dynamic one-offs only
```

`styled-jsx` scopes selectors to the component subtree — good for **small overrides** in Next pages without global CSS file sprawl.

```txt
Global CSS     → layout tokens, resets (once in root)
Component CSS  → module or styled-jsx
Design system  → shared Button variants
```

---

## Standard config / commands

### CSS Modules (recommended default in Vite)

```tsx
import styles from "./Card.module.css";

export function Card({ title }: { title: string }) {
  return <article className={styles.card}><h2 className={styles.title}>{title}</h2></article>;
}
```

```css
/* Card.module.css */
.card { padding: 1rem; border-radius: 8px; }
.title { font-size: 1.125rem; }
```

### styled-jsx (Next.js)

```tsx
export function Badge({ color }: { color: string }) {
  return (
    <>
      <span className="badge">New</span>
      <style jsx>{`
        .badge {
          background: ${color};
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
        }
      `}</style>
    </>
  );
}
```

### Dynamic values — prefer CSS variables

```tsx
<div style={{ ["--accent" as string]: color }} className={styles.box} />
/* .box { background: var(--accent); } */
```

Avoid huge inline objects recreated every render ([[referential equality]] matters for memoized children).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Styles not applied (Modules) | Wrong import | `import s from './x.module.css'` |
| Flash unstyled (FOUC) | CSS load order | [[css/Flash of Unstyled Content]] |
| styled-jsx not working | Not Next / plugin | Use Modules or Tailwind in Vite |
| Specificity wars | Global !important | Scope with Modules |
| Hydration class mismatch | Random class gen | Stable build config |

---

## Gotchas

> [!WARNING]
> **Runtime CSS-in-JS** — extra bundle + insert cost; RSC apps often prefer static CSS ([[RSC (React Server Component boundaries)]]).

> [!WARNING]
> **styled-jsx global** — `<style jsx global>` affects entire app — use sparingly.

---

## When NOT to use

- **Design system at scale** — Tailwind + component variants ([[css/tailwindcss]]), not per-component `<style jsx>`.
- **Animation-heavy** — [[Framer motion]] + CSS transforms, not inline everything.
- **Plain static site** — external CSS file sufficient.

---

## Related

[[css/tailwindcss]] · [[css/scss]] · [[Optimizing performance]] · [[React build]]
