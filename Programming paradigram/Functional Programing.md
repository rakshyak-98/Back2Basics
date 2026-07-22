[[Programming paradigram/purely declarative]] [[Operating System/Stack based programming language]]

# Functional programming

> Compose pure functions and immutable data — minimize shared mutable state; side effects at the edges.

## Mental model

Core ideas: **pure functions** (same input → same output), **immutability**, **first-class functions**, **referential transparency**. State changes via new values, not mutation. Higher-order functions (`map`, `filter`, `reduce`) replace many loops. IO/monads/effects pushed to boundaries ("functional core, imperative shell").

```
input → f(g(h(x))) → output
no hidden globals; mutation → new copy
```

## Standard config / commands

### Pure function shape

```js
// pure
function addTax(price, rate) {
  return price * (1 + rate);
}

// impure — hide at boundary
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}
```

### HOC patterns

```js
const nums = [1, 2, 3];
const doubled = nums.map(x => x * 2);
const sum = nums.reduce((a, b) => a + b, 0);
```

### Immutable update (JS)

```js
const next = { ...user, name: 'Ada' };
const nextList = [...items, newItem];
```

### React alignment

```jsx
// prefer derived state, not mutate props/state in place
const visible = items.filter(i => i.active);
```

## Triage (when things break)

| Smell | Check | Fix |
|-------|-------|-----|
| Stale UI | Mutated object in place | New reference for React deps |
| Heisenbug | Global mutable cache | Pass deps explicitly |
| Stack overflow | Deep recursion | Tail-call (where supported) or loop |
| Performance | Excess copying | Structural sharing (Immer), persistent DS |
| "Same input diff output" | Hidden Date/random/network | Inject clock/RNG; isolate IO |

## Gotchas

> [!WARNING]
> **`map` without return** — accidental `undefined` array.
>
> **Shallow copy nested objects** — still aliased inner fields.
>
> **FP in JS without types** — easy to pass wrong arity; use TS.

## When NOT to use

- Don't clone huge graphs every tick in hot paths — profile first.
- Don't ban all mutation in low-level perf code (games, codecs) — isolate instead.

## Related

[[Programming paradigram/purely declarative]] [[React/React data management]] [[Design pattern/Static Members]]
