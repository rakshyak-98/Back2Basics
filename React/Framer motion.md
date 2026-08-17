[[react hooks]] [[React State management]] [[React Architecture]]

# Framer Motion

> React animation library — declarative motion components and gestures on top of the DOM.

```txt
        Framer Motion ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you animate without layout thrash, and when CSS transiti…

## Sources
- [Framer Motion docs](https://www.framer.com/motion/) — deep-dive
- [React — useEffect](https://react.dev/reference/react/useEffect) — overview

## Key Concepts
- **motion components:** `motion.div` instead of `div`.
- **Animate presence:** exit animations for conditional trees.
- **Layout:** `layout` prop for shared-element style transitions.


- **Core:** Framer Motion wraps elements in `motion.*` components with animate/transition…

## Technical Details
```tsx
import { motion } from 'framer-motion'
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
```

## Mistakes to Avoid
- **Mistake:** Animating huge lists without virtualization
- **Mistake:** Fighting reduced-motion accessibility preferences

## Pros/Cons or Trade-offs
- **Pro:** Rich gestures and orchestration in React trees.
- **Con:** Bundle weight — prefer CSS for simple fades.

## Comparison
- vs CSS transitions: use CSS for simple opacity/transform; Framer for orchestration/gestures.


### Use cases
- Modal enter/exit and tab indicator slide using layout animations instead of b…
