[[Optimizing performance]] [[react hooks]] [[React State management]] [[debouncing]]

# Referential equality

> **`===` for objects/functions** — same reference means "unchanged" to React memoization — **React reconciliation**.

---

## Mental model

Primitives compared by **value**; objects, arrays, functions by **reference**:

```javascript
{} === {}           // false
fn === fn           // true only if same function object
useState setter     // stable reference (usually)
() => {} each render // new reference every time
```

React re-renders when state/props change. **`React.memo`**, **`useMemo`**, **`useCallback`**, **`useEffect` deps`** use `Object.is` (like `===` for refs).

```txt
Parent re-render
  → inline onClick = () => {}  // new ref
  → memo(Child) still re-renders (props "changed")
```

Stable references let you **skip** subtree work ([[Optimizing performance]]).

---

## Standard config / commands

### Stable callback with useCallback

```tsx
const onSave = useCallback(() => {
  save(draft);
}, [draft, save]);

return <MemoizedEditor onSave={onSave} />;
```

### Stable object — useMemo or split props

```tsx
const config = useMemo(() => ({ theme, locale }), [theme, locale]);
// Better: pass theme and locale as separate props
```

### Functional update avoids stale state + extra deps

```tsx
setCount((c) => c + 1); // no need for count in deps
```

### Context value stability

```tsx
const value = useMemo(() => ({ user, logout }), [user, logout]);
return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
```

See [[React State management]] — don't memo everything; profile first.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| memo useless | Unstable prop refs | useCallback/useMemo upstream |
| useEffect infinite loop | Object/array in deps | Primitive deps or memoize |
| Stale closure in callback | Empty deps but uses state | Functional update or include deps |
| Context consumers all update | New `{}` value each render | useMemo context value |
| Zustand/selectors fine | External store uses snapshot | Select primitives |

---

## Gotchas

> [!WARNING]
> **Premature useCallback everywhere** — costs memory; only for heavy children or effect deps.

> [!WARNING]
> **Deep equality in memo** — React doesn't do it; structural sharing libraries (Immer) still change top ref when draft committed.

---

## When NOT to use

- **Cheap leaf components** — memo + callback overhead > re-render cost.
- **Server Components** — client referential equality rules don't apply on server.
- **Replacing proper state design** — lift or colocate instead of memo band-aids.

---

## Related

[[Optimizing performance]] · [[react hooks]] · [[React State management]] · [[debouncing]] · [[Lexical environment]]
