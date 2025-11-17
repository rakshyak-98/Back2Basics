React's render must stay pure (no side effect when component is rendering).
`useEffect()` lets you run code after render, where side effect are allowed. 

> [!NOTE]
> - `useEffect()` runs after render.

## Order of `useEffect`
all `useEffect` hooks in a component run in the order they are written in the code, every time their dependency array changes (or on mount if empty).

|Dependency array|When does it run?|Order relative to other effects|
|---|---|---|
|`useEffect(() => {}, [])`|Only once → after **first render** (mount)|In code order|
|`useEffect(() => {}, [dep1])`|After **every render** when `dep1` changed (including first render)|In code order|
|`useEffect(() => {}, [a, b])`|After render when **a** OR **b** changed|In code order|
|`useEffect(() => {}, deps)`|After render when **any** dependency changed (shallow comparison)|In code order|
|`useEffect(() => { return cleanup }, ...)`|Cleanup runs **before** next effect and on unmount|Cleanup also in code order|