**A functional component will render for one of three reasons:**
- Then component was not in the component tree before and is now.
- The parent component just re-rendered.
- The component uses a hook that has flagged this component for re-render.

> [!NOTE] React might batch rendering after several of these things happen.

if a state value changes and the parent component re-renders, for example, the component might re-render once, or it might re-render twice.
### Memoization 
- Property memoization is relevant for objects and arrays created inline, and even more so for functions, which is the primary reason for the existence of the `useCallback` hook and why it is used so often in React.
- to prevent expensive recalculations
- to maintain referential equality

> [!NOTE] if any value in the dependency array has changed since the component was last rendered

> [!NOTE] `useMemo` will not recompute because it only tracks the reference, not the content.

### Memoize functions with `useCallback`

```javascript
function useCallback(fn, deps){
	return useMemo(() => fn, deps)
}
```
- `useCallback` makes memoized callback where referential equality is desired, and is never used to prevent expensive calculations.

> [!WARNING] we memoize functions more often than other types of values.

- An empty array in an effect hook indicates that it runs only on mount, whereas a nonempty array indicates that the hook runs on mount and every time the mentioned dependencies update.

> [!NOTE] A dependency is any local variable that exists locally in the component scope but not any variable that also exists outside the component scope.
