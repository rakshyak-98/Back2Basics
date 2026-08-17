[[npm]] [[node package json]]

# moment

> Once-dominant JavaScript date library — parse, format, and manipulate calendar times (now in maintenance mode; prefer modern alternatives for new code).





## Interview Relevance
Interviewers use Moment to probe mutability pitfalls, timezone mistakes, and whether you know it is legacy — choosing `Intl`, `Temporal` (where available), or libraries like Luxon/Day.js for greenfield work.

## Sources
- [Moment.js documentation](https://momentjs.com/docs/) — deep-dive
- [Moment project status](https://momentjs.com/docs/#/-project-status/) — overview
- [MDN — `Intl.DateTimeFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) — overview

## Core Definition
Moment wraps JavaScript `Date` with a fluent API for parsing, formatting, comparing, and arithmetic. The project is in maintenance mode: no new features; existing apps may keep it, new apps should pick a smaller or immutable alternative.

## Key Concepts
- **Mutable by default:** `moment().add(1, "day")` mutates the instance → clone before mutating when sharing references.
- **Parse with format:** `moment(str, "YYYY-MM-DD")` avoids ambiguous free-parse behavior.
- **Display vs instant:** formatting for humans is locale/timezone sensitive — be explicit about UTC versus local.
- **Bundle size:** Moment is large historically (especially with locales) → tree-shaking-friendly libs win in browsers.
- **Maintenance mode:** security/critical fixes only — plan migration rather than expanding usage.

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

## Real-World Applications
Legacy dashboards and APIs still format timestamps with Moment; new services often keep Moment only at the edges until migrated.

**Example:** A report generator formats `created_at` with `moment.utc(ts).format("YYYY-MM-DD")` so all regions see the same calendar day.

## Pros/Cons or Trade-offs
- **Pro:** Familiar API; still fine for frozen legacy codepaths.
- **Con:** Mutable API and large footprint; poor fit for new frontends.
- **Con:** Maintenance mode — do not build new features on it.

## Comparison
- vs native `Date` / `Intl`: sufficient for many display-only needs without a dependency.
- vs Day.js / Luxon / Temporal: smaller or immutable models; better default for new projects.

## Mistakes to Avoid
- Calling `.add` / `.subtract` on a shared moment without `.clone()`.
- Parsing locale-ambiguous strings without an explicit format.
- Adding Moment to a new greenfield app without checking modern alternatives.
