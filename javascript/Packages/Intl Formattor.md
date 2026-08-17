[[javascript]] [[Packages]] [[moment]] [[LF and CRLF]]

# Intl Formattor

> `Intl.*` — built-in locale formatting for numbers, dates, lists, plurals, and collation (no Moment required for basics).

```txt
        Intl Formattor ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **Intl Formattor** to see if you understand what it does o…

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

## Mistakes to Avoid
- **Mistake:** **Filename typo**
- **Mistake:** **Polyfills still needed on ancient engines**
- **Mistake:** **Don’t parse with formatters**
- **Mistake:** **Wrong separators:** check Locale typo
- **Mistake:** **Currency code error:** check Bad ISO currency
- **Mistake:** **Hydration mismatch:** check Server locale ≠ client
- **Mistake:** **Slow lists:** check New formatter per row
- **Mistake:** **Sort “wrong”:** check Default `>` compare; fix: Use `Collator`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (`Intl.*` — built-in locale formatting for numbers, dates, lists, plurals, and co…).
- **Con / when not:** **Timezone-heavy calendars**
- **Con / when not:** **ICU message syntax apps**
- **Con / when not:** **Pixel-perfect custom typography**

## Comparison
- vs [[Packages]]: know when each applies


### Use cases
- In production APIs and tooling, **Intl Formattor** shows up whenever teams sh…
