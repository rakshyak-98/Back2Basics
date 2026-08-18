[[javascript]] [[prototype]] [[Packages/Immer]]

# primitive non-primitive values

> Primitives (number, string, bool, null, undefined, symbol, bigint) are copied by value; objects/arrays/functions are references.

## Mental model

**Say it in one breath:** Assigning a primitive copies the bit pattern; assigning an object copies the pointer — mutate via one variable, the other sees it.

```txt
let a = 1; let b = a; b = 2        // a still 1
let x = { n: 1 }; let y = x; y.n = 2  // x.n is 2
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **primitive** | Immutable value types | “Strings feel mutable but rebind.” |
| --- | --- | --- |
| **reference** | Pointer to heap object | “Equality is identity for objects.” |
| **shallow copy** | New object, same nested refs | “`{...obj}` / `slice`.” |

## Standard config / commands

```js
Object.is(NaN, NaN) // true — better than === for NaN
const copy = { ...obj } // shallow
const deep = structuredClone(obj) // deep (modern)
```

| Check | Meaning |
| --- | --- |
| `===` on objects | Same reference |
| `===` on primitives | Same value |
| `typeof null` | `"object"` quirk |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Unexpected shared mutation | Passed object around | Clone / immutable update |
| `NaN === NaN` false | Used === | `Number.isNaN` / `Object.is` |
| Compare objects by value | === fails | deep-equal helper |
| Accidental box | `new String` | Prefer primitives |

## Gotchas

> [!WARNING]
> **`typeof null === 'object'`** — historical bug; check `null` explicitly.

> [!WARNING]
> **String immutability** — `s[0] = 'X'` does nothing in strict mental model; reassign.

## When NOT to use

- **Over-cloning huge graphs** — share immutably with care ([[Packages/Immer]]).
- **Micro-optimizing primitives** — readability first.

## Related

[[prototype]] [[Packages/Immer]] [[Destructuring]]
