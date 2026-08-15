[[javascript]] [[prototype]] [[Packages/Immer]] [[Destructuring]]

# primitive non-primitive values

> Primitives (number, string, bool, null, undefined, symbol, bigint) are copied by value; objects/arrays/functions are references.

## Interview Relevance

Interviewers use **primitive non-primitive values** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **primitive**, **reference**, **shallow copy**.

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

## Real-World Applications

In production APIs and tooling, **primitive non-primitive values** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`typeof null === 'object'`** — historical bug; check `null` explicitly; **String immutability** — `s[0] = 'X'` does nothing in strict mental model; reassign.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Primitives (number, string, bool, null, undefined, symbol, bigint) are copied by…).
- **Con / when not:** **Over-cloning huge graphs** — share immutably with care ([[Packages/Immer]]).
- **Con / when not:** **Micro-optimizing primitives** — readability first.

## Comparison

vs [[prototype]]: know when each applies — do not treat them as interchangeable. vs [[Packages/Immer]]: know when each applies — do not treat them as interchangeable. vs [[Destructuring]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`typeof null === 'object'`** — historical bug; check `null` explicitly.
- **String immutability** — `s[0] = 'X'` does nothing in strict mental model; reassign.
- **Unexpected shared mutation:** check Passed object around; fix: Clone / immutable update
- **`NaN === NaN` false:** check Used ===; fix: `Number.isNaN` / `Object.is`
- **Compare objects by value:** check === fails; fix: deep-equal helper
- **Accidental box:** check `new String`; fix: Prefer primitives
