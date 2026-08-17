[[Optimizing performance]] [[react hooks]] [[React State management]] [[debouncing]] [[Lexical environment]]

# Referential equality

> Referential equality — primitives compared by value; objects, arrays, functions by reference:





## Interview Relevance
Interviewers probe **Referential equality** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Wikipedia — referential equality](https://en.wikipedia.org/wiki/referential_equality) — overview

## Core Definition
Primitives compared by **value**; objects, arrays, functions by **reference**:

## Key Concepts
- Primitives compared by **value**; objects, arrays, functions by **reference**:
- React re-renders when state/props change. **`React.memo`**, **`useMemo`**, **`useCallback`**, **`useEffect` deps`** use `Object.is` (like `===` for refs).
- Stable references let you **skip** subtree work ([[Optimizing performance]]).

## Technical Details
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

## Real-World Applications
In production APIs and tooling, **referential equality** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Premature useCallback everywhere** — costs memory; only for heavy children or effect deps; **Deep equality in memo** — React doesn't do it; structural sharing libraries (Immer) still change top ref when draft committed.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Referential equality — primitives compared by value; objects, arrays, functions …).
- **Con / when not:** **Cheap leaf components** — memo + callback overhead > re-render cost.
- **Con / when not:** **Server Components** — client referential equality rules don't apply on server.
- **Con / when not:** **Replacing proper state design** — lift or colocate instead of memo band-aids.

## Comparison
vs [[Optimizing performance]]: know when each applies — do not treat them as interchangeable. vs [[react hooks]]: know when each applies — do not treat them as interchangeable. vs [[React State management]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Premature useCallback everywhere** — costs memory; only for heavy children or effect deps.
- **Deep equality in memo** — React doesn't do it; structural sharing libraries (Immer) still change top ref when draft committed.
- **memo useless:** check Unstable prop refs; fix: useCallback/useMemo upstream
- **useEffect infinite loop:** check Object/array in deps; fix: Primitive deps or memoize
- **Stale closure in callback:** check Empty deps but uses state; fix: Functional update or include deps
- **Context consumers all update:** check New `{}` value each render; fix: useMemo context value
- **Zustand/selectors fine:** check External store uses snapshot; fix: Select primitives
