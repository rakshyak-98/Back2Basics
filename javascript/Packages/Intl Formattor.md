[[javascript]] [[Packages]] [[moment]] [[LF and CRLF]]

# Intl Formattor

> `Intl.*` — built-in locale formatting for numbers, dates, lists, plurals, and collation (no Moment required for basics).





## Interview Relevance
Interviewers probe **Intl Formattor** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Wikipedia — Intl Formattor](https://en.wikipedia.org/wiki/Intl_Formattor) — overview

## Technical Details
```txt
value + locale + options ──Intl.*Format──► string
```

| API | Job |
|-----|-----|
| `NumberFormat` | Numbers / currency / % |
| `DateTimeFormat` | Dates/times |
| `RelativeTimeFormat` | “yesterday”, “in 3 days” |
| `ListFormat` | “A, B, and C” |
| `Collator` | Locale-aware sort |
| `PluralRules` | one/other/… |

```js
new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(123456)
new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' }).format(new Date())
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day')
;['Zebra', 'äpfel'].sort(new Intl.Collator('de').compare)
new Intl.ListFormat('en', { type: 'conjunction' }).format(['A', 'B', 'C'])
```

| Knob | Why it matters |
|------|----------------|
| Locale string | UI language ≠ currency |
| `timeZone` | Server UTC vs user TZ |
| Cache formatters | Constructing is relatively expensive |

## Real-World Applications
In production APIs and tooling, **Intl Formattor** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Filename typo** — API is `Intl`, not a separate “Formattor” package; **Polyfills still needed on ancient engines** — check caniuse for `Segmenter` etc.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (`Intl.*` — built-in locale formatting for numbers, dates, lists, plurals, and co…).
- **Con / when not:** **Timezone-heavy calendars** — consider Temporal / a date lib.
- **Con / when not:** **ICU message syntax apps** — FormatJS / bilingual message frameworks.
- **Con / when not:** **Pixel-perfect custom typography** — design system components wrapping Intl.

## Comparison
vs [[Packages]]: know when each applies — do not treat them as interchangeable. vs [[moment]]: know when each applies — do not treat them as interchangeable. vs [[LF and CRLF]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Filename typo** — API is `Intl`, not a separate “Formattor” package.
- **Polyfills still needed on ancient engines** — check caniuse for `Segmenter` etc.
- **Don’t parse with formatters** — formatting ≠ robust date parsing.
- **Wrong separators:** check Locale typo; fix: Verify `navigator.language`
- **Currency code error:** check Bad ISO currency; fix: Use valid `currency`
- **Hydration mismatch:** check Server locale ≠ client; fix: Fix locale source of truth
- **Slow lists:** check New formatter per row; fix: Reuse one instance
- **Sort “wrong”:** check Default `>` compare; fix: Use `Collator`
