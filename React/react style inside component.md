[[css/scss]] [[css/tailwindcss]] [[Optimizing performance]] [[React build]]

# React style inside component

> React style inside component — CSS Modules (*.module.css) → build-time scoped class names (Vite default)

```txt
        React style inside ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use React style inside component to test whether you can apply t…

## Sources
- [Wikipedia — react style inside component](https://en.wikipedia.org/wiki/react_style_inside_component) — overview

## Key Concepts
Options for component-local styling:

- **Note:** `styled-jsx` scopes selectors to the component subtree

```txt
Global CSS     → layout tokens, resets (once in root)
Component CSS  → module or styled-jsx
Design system  → shared Button variants
```

## Technical Details
```txt
CSS Modules (*.module.css)   → build-time scoped class names (Vite default)
Tailwind utility classes      → [[css/tailwindcss]] in className
styled-jsx                    → <style jsx> injected per component (Next)
CSS-in-JS runtime             → styled-components (runtime cost)
Inline style={{}}             → dynamic one-offs only
```

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

- Avoid huge inline objects recreated every render ([[referential equality]] ma…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Styles not applied (Modules) | Wrong import | `import s from './x.module.css'` |
| Flash unstyled (FOUC) | CSS load order | [[css/Flash of Unstyled Content]] |
| styled-jsx not working | Not Next / plugin | Use Modules or Tailwind in Vite |
| Specificity wars | Global !important | Scope with Modules |
| Hydration class mismatch | Random class gen | Stable build config |

- **Mistake:** **Runtime CSS-in-JS**
- **Mistake:** **styled-jsx global**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Design system at scale**
- **Con / skip when:** **Animation-heavy**
- **Con / skip when:** **Plain static site** — external CSS file sufficient.

## Comparison
- vs [[css/tailwindcss]]: **Design system at scale**
- vs [[Framer motion]]: **Animation-heavy**


### Use cases
- Apply React style inside component in feature code where the Key Concepts mat…
