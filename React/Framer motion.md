[[react hooks]] [[React State management]] [[React Architecture]]

# Framer Motion

> React animation library — declarative motion components and gestures on top of the DOM.

## Interview Relevance

Interviewers ask how you animate without layout thrash, and when CSS transitions beat a JS animation library.

## Sources

- [Framer Motion docs](https://www.framer.com/motion/) — deep-dive
- [React — useEffect](https://react.dev/reference/react/useEffect) — overview

## Core Definition

Framer Motion wraps elements in `motion.*` components with animate/transition props and optional layout animations.

## Key Concepts

- **motion components:** `motion.div` instead of `div`.
- **Animate presence:** exit animations for conditional trees.
- **Layout:** `layout` prop for shared-element style transitions.

## Technical Details

```tsx
import { motion } from 'framer-motion'
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
```

## Real-World Applications

Modal enter/exit and tab indicator slide using layout animations instead of brittle CSS keyframe sets.

## Pros/Cons or Trade-offs

- **Pro:** Rich gestures and orchestration in React trees.
- **Con:** Bundle weight — prefer CSS for simple fades.

## Comparison

- vs CSS transitions: use CSS for simple opacity/transform; Framer for orchestration/gestures.

## Mistakes to Avoid

- Animating huge lists without virtualization.
- Fighting reduced-motion accessibility preferences.
