[[Optimizing performance]] [[react hooks]] [[React State management]] [[debouncing]] [[Lexical environment]]

# Referential equality

> Referential equality — primitives compared by value; objects, arrays, functions by reference:

```txt
        Referential equali ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Referential equality** to see if you understand what it …

## Sources
- [Wikipedia — referential equality](https://en.wikipedia.org/wiki/referential_equality) — overview

## Key Concepts
- **Primitives compared:** Primitives compared by **value**; objects, arrays, functions by **reference**:
- **React re-renders:** React re-renders when state/props change
- **Stable references:** Stable references let you **skip** subtree work ([[Optimizing performance]]).


- **Core:** Primitives compared by **value**; objects, arrays, functions by **reference**:

## Technical Details
- Primitives compared by **value**; objects, arrays, functions by **reference**:

```javascript
{} === {}           // false
fn === fn           // true only if same function object
useState setter     // stable reference (usually)
() => {} each render // new reference every time
```

- React re-renders when state/props change.
- **`React.memo`:** , **`useMemo`**, **`useCallback`**, **`useEffect` deps`** use…

```txt
Parent re-render
  → inline onClick = () => {}  // new ref
  → memo(Child) still re-renders (props "changed")
```

- Stable references let you **skip** subtree work ([[Optimizing performance]]).

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

- See [[React State management]] — don't memo everything; profile first.

## Mistakes to Avoid
- **Mistake:** **Premature useCallback everywhere**
- **Mistake:** **Deep equality in memo**
- **Mistake:** **memo useless:** check Unstable prop refs
- **Mistake:** **useEffect infinite loop:** check Object/array in deps
- **Mistake:** **Stale closure in callback:** check Empty deps but uses state
- **Mistake:** **Context consumers all update:** check New `{}` value each rend…
- **Mistake:** **Zustand/selectors fine:** check External store uses snapshot

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Referential equality — primitives compared by value; objects, arrays, functions …).
- **Con / when not:** **Cheap leaf components**
- **Con / when not:** **Server Components**
- **Con / when not:** **Replacing proper state design**

## Comparison
- vs [[Optimizing performance]]: know when each applies


### Use cases
- In production APIs and tooling, **referential equality** shows up whenever te…
