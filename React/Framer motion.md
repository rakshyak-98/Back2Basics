[[Optimizing performance]] [[react hooks]] [[React build]] [[css/Animation]]

# Framer Motion

> Declarative animation library for React — `motion` components, variants, layout transitions — **Motion (formerly Framer Motion) docs**.

---

## Mental model

Framer Motion wraps DOM nodes as **`motion.div`** etc. Animate by changing props (`animate`, `initial`, `exit`) or **variants** (named state maps).

```txt
initial → animate → exit (AnimatePresence)
variants cascade parent → children
layout → FLIP-style layout animations on reflow
```

Runs on **main thread** (with WAAPI where possible). Heavy animation on large lists competes with React render — prefer `transform`/`opacity`, not `width`/`top`.

| API | Use |
|-----|-----|
| `motion.*` | Animated element |
| `variants` | Orchestrated multi-step |
| `AnimatePresence` | Mount/unmount exit animations |
| `layout` | Auto layout shift animation |
| `useReducedMotion` | Accessibility respect |

---

## Standard config / commands

```tsx
import { motion, AnimatePresence } from "framer-motion";

const panel = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
};

export function SlidePanel({ open }: { open: boolean }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.aside
          key="panel"
          variants={panel}
          initial="hidden"
          animate="visible"
          exit="exit"
          transition={{ duration: 0.2 }}
        >
          Content
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
```

### Respect reduced motion

```tsx
import { useReducedMotion } from "framer-motion";

const reduce = useReducedMotion();
<motion.div animate={{ opacity: 1 }} transition={{ duration: reduce ? 0 : 0.3 }} />
```

### Layout animation (careful on lists)

```tsx
<motion.div layout layoutId="shared-card" />
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Exit animation skipped | Missing `AnimatePresence` | Wrap conditional; unique `key` |
| Janky list scroll | Animating layout/width | Use transform only; virtualize list |
| Flash on hydration | SSR mismatch | `initial={false}` after mount |
| Bundle size spike | Full import | `LazyMotion` + `domAnimation` feature pack |
| Children don't stagger | Variants not on parent | `variants` + `staggerChildren` on parent |

---

## Gotchas

> [!WARNING]
> **Animating `height: auto`** — expensive; use `layout` or fixed max-height hack with measure.

> [!WARNING]
> **Modal focus trap** — motion doesn't handle a11y; pair with focus management.

---

## When NOT to use

- **CSS-only hover/focus** — Tailwind transitions cheaper ([[css/Animation]]).
- **Canvas/WebGL games** — use RAF loop or dedicated engine.
- **Critical path LCP hero** — prefer CSS; defer motion library.

---

## Related

[[Optimizing performance]] · [[css/Animation]] · [[react hooks]] · [[React build]]
