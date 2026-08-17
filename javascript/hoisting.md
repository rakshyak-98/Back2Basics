[[javascript]] [[prototype]] [[IIFC]] [[self-defining functions]]

# hoisting

> Declarations are visible in their scope before the line runs — `var`/`function` hoist differently from `let`/`const`.





## Interview Relevance
Interviewers use **hoisting** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **TDZ**, **function decl**, **function expr**.

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

## Real-World Applications
In production APIs and tooling, **hoisting** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`var` in loops with async** — classic closure bug; use `let`; **Class declarations** — also TDZ until evaluated.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Declarations are visible in their scope before the line runs — `var`/`function` …).
- **Con / when not:** **Designing APIs around hoisting** — write top-down clarity instead.
- **Con / when not:** **`var` in new code** — prefer `let`/`const`.

## Comparison
vs [[prototype]]: know when each applies — do not treat them as interchangeable. vs [[IIFC]]: know when each applies — do not treat them as interchangeable. vs [[self-defining functions]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`var` in loops with async** — classic closure bug; use `let`.
- **Class declarations** — also TDZ until evaluated.
- **`undefined` unexpectedly:** check `var` use-before-assign; fix: Use `let`/`const`; reorder
- **ReferenceError TDZ:** check `let` before line; fix: Move declaration up
- **Not a function:** check Called const fn before init; fix: Reorder
- **Duplicate decl errors:** check Redeclare `let`; fix: One binding
