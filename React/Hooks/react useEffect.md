> [!INFO]
> `useEffect` runs **after render** when its dependency array value changes.

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

> [!WARNING]
> You should avoid using `` for purely derived (computed) state like splitting a full name. Instead, compute it directly in the render or with `useMemo`.

### Call fetch api in `useEffect`

```js
useEffect(() => {
  const controller = new AbortController(); // For fetch
  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') console.error(err);
    });

  return () => controller.abort(); // Cancels the first request on simulated unmount
}, []);

```

- The first fetch gets aborted during the simulation → only the second completes.
- Safe and mirrors real cleanup needs.

> [!INFO]
> - If it's a POST or mutating request, move it to an event handler (not a mount effect).
> - GET requests are usually safe to duplicate (same result, no side effects).

## How to Handle State Synchronization Between Multiple useEffect Hooks

> [!NOTE]
> In React, when one `useEffect` updates a state value, any other `useEffect` that depends on that state will automatically run on the *next render*.