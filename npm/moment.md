[[npm]] [[node package json]]

# moment

> Once-dominant JavaScript date library — parse, format, and manipulate calendar times (now in maintenance mode; prefer modern alternatives for new code).

```txt
        moment ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use Moment to probe mutability pitfalls, timezone mistakes, and …

## Sources
- [Moment.js documentation](https://momentjs.com/docs/) — deep-dive
- [Moment project status](https://momentjs.com/docs/#/-project-status/) — overview
- [MDN — `Intl.DateTimeFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) — overview

## Key Concepts
- **Mutable by default:** `moment().add(1, "day")` mutates the instance → clone before mutating when sh…
- **Parse with format:** `moment(str, "YYYY-MM-DD")` avoids ambiguous free-parse behavior.
- **Display vs instant:** formatting for humans is locale/timezone sensitive
- **Bundle size:** Moment is large historically (especially with locales) → tree-shaking-friendl…
- **Maintenance mode:** security/critical fixes only — plan migration rather than expanding usage.


- **Core:** Moment wraps JavaScript `Date` with a fluent API for parsing, formatting, com…

## Technical Details
```js
moment("2026-03-24")                       // parse from string (prefer explicit format)
moment(new Date())                         // from JS Date
moment("2026-03-24", "YYYY-MM-DD")         // safer parse

moment().format("YYYY-MM-DD")              // "2026-03-24"
moment().format("MMMM DD")                 // "March 24"

moment().add(1, "days")
moment().subtract(1, "months")

moment(a).isSame(moment(b), "day")
moment(a).isBefore(moment(b), "day")
moment(a).isAfter(moment(b), "day")
moment(a).diff(moment(b), "days")

moment().toDate()                          // back to native Date
moment().clone().add(1, "day")             // avoid shared mutation
```

| Symptom | Likely cause |
|---------|--------------|
| Off-by-one day near midnight | Local timezone vs UTC mix |
| “Invalid date” | Ambiguous parse; missing format string |
| Shared state bugs | Mutated a moment still held elsewhere |
| Huge browser bundle | Full Moment + locales imported |

## Mistakes to Avoid
- **Mistake:** Calling `.add` / `.subtract` on a shared moment without `.clone(…
- **Mistake:** Parsing locale-ambiguous strings without an explicit format
- **Mistake:** Adding Moment to a new greenfield app without checking modern al…

## Pros/Cons or Trade-offs
- **Pro:** Familiar API; still fine for frozen legacy codepaths.
- **Con:** Mutable API and large footprint; poor fit for new frontends.
- **Con:** Maintenance mode — do not build new features on it.

## Comparison
- vs native `Date` / `Intl`: sufficient for many display-only needs without a dependency.
- vs Day.js / Luxon / Temporal: smaller or immutable models; better default for new projects.


### Use cases
- Legacy dashboards and APIs still format timestamps with Moment

- **Example:** A report generator formats `created_at` with `moment.utc(ts).for…
