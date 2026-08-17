[[javascript]] [[prototype]] [[Packages/Immer]] [[Destructuring]]

# primitive non-primitive values

> Primitives (number, string, bool, null, undefined, symbol, bigint) are copied by value; objects/arrays/functions are references.

```txt
        primitive non-prim ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **primitive non-primitive values** to check whether you can …

## Sources
- [Wikipedia — primitive non-primitive values](https://en.wikipedia.org/wiki/primitive_non-primitive_values) — overview

## Key Concepts
- **primitive:** Immutable value types — Strings feel mutable but rebind.
- **reference:** Pointer to heap object — Equality is identity for objects.
- **shallow copy:** New object, same nested refs — `{...obj}` / `slice`.

## Technical Details
```txt
let a = 1; let b = a; b = 2        // a still 1
let x = { n: 1 }; let y = x; y.n = 2  // x.n is 2
```

```js
Object.is(NaN, NaN) // true — better than === for NaN
const copy = { ...obj } // shallow
const deep = structuredClone(obj) // deep (modern)
```

| Check | Meaning |
|-------|---------|
| `===` on objects | Same reference |
| `===` on primitives | Same value |
| `typeof null` | `"object"` quirk |

## Mistakes to Avoid
- **Mistake:** **`typeof null === 'object'`**
- **Mistake:** **String immutability**
- **Mistake:** **Unexpected shared mutation:** check Passed object around
- **Mistake:** **`NaN === NaN` false:** check Used ===
- **Mistake:** **Compare objects by value:** check === fails
- **Mistake:** **Accidental box:** check `new String`; fix: Prefer primitives

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Primitives (number, string, bool, null, undefined, symbol, bigint) are copied by…).
- **Con / when not:** **Over-cloning huge graphs**
- **Con / when not:** **Micro-optimizing primitives** — readability first.

## Comparison
- vs [[prototype]]: know when each applies


### Use cases
- In production APIs and tooling, **primitive non-primitive values** shows up w…
