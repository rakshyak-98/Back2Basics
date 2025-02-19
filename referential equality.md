means that a function reference remains the same between renders unless dependencies change.

### Why it matters?
- React re-renders components when props or state change.
- If a new function is created on every render, it breaks referential equality, causing unnecessary re-renders.