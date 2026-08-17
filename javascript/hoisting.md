[[javascript]] [[prototype]] [[IIFC]] [[self-defining functions]]

# hoisting

> Declarations are visible in their scope before the line runs — `var`/`function` hoist differently from `let`/`const`.

```txt
        hoisting ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **hoisting** to check whether you can explain the mechanism …

## Sources
- [MDN — Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting) — deep-dive
- [Wikipedia — hoisting](https://en.wikipedia.org/wiki/hoisting) — overview

## Key Concepts
- **TDZ:** Temporal dead zone — Binding exists but unread until init.
- **function decl:** Hoisted body — Can call above definition.
- **function expr:** Not hoisted as fn — `const f = () =>` is TDZ like const.

## Technical Details
```txt
console.log(a) // undefined with var; TDZ ReferenceError with let
var a = 1
let b = 2
```

```js
// Prefer
const x = 1
function f() {}
// Avoid relying on var hoisting
```

| Form | Before init |
|------|-------------|
| `var` | `undefined` |
| `let`/`const` | TDZ error |
| `function foo(){}` | Callable |
| `const foo = function(){}` | TDZ |

## Mistakes to Avoid
- **Mistake:** **`var` in loops with async** — classic closure bug; use `let`
- **Mistake:** **Class declarations** — also TDZ until evaluated
- **Mistake:** **`undefined` unexpectedly:** check `var` use-before-assign
- **Mistake:** **ReferenceError TDZ:** check `let` before line
- **Mistake:** **Not a function:** check Called const fn before init
- **Mistake:** **Duplicate decl errors:** check Redeclare `let`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Declarations are visible in their scope before the line runs — `var`/`function` …).
- **Con / when not:** **Designing APIs around hoisting**
- **Con / when not:** **`var` in new code** — prefer `let`/`const`.

## Comparison
- vs [[prototype]]: know when each applies


### Use cases
- In production APIs and tooling, **hoisting** shows up whenever teams ship Nod…
