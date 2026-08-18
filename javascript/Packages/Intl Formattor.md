[[javascript]] [[Packages]]

# Intl Formattor

> `Intl.*` — built-in locale formatting for numbers, dates, lists, plurals, and collation (no Moment required for basics).

## Mental model

**Say it in one breath:** Pass a BCP 47 locale + options; the engine formats with CLDR data. Prefer `Intl` over hand-rolled separators or shipping Moment just for dates.

```txt
value + locale + options ──Intl.*Format──► string
```

| API | Job |
| --- | --- |
| `NumberFormat` | Numbers / currency / % |
| `DateTimeFormat` | Dates/times |
| `RelativeTimeFormat` | “yesterday”, “in 3 days” |
| `ListFormat` | “A, B, and C” |
| `Collator` | Locale-aware sort |
| `PluralRules` | one/other/… |

## Standard config / commands

```js
new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(123456)
new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' }).format(new Date())
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day')
;['Zebra', 'äpfel'].sort(new Intl.Collator('de').compare)
new Intl.ListFormat('en', { type: 'conjunction' }).format(['A', 'B', 'C'])
```

| Knob | Why it matters |

| Locale string | UI language ≠ currency |
| --- | --- |
| `timeZone` | Server UTC vs user TZ |
| Cache formatters | Constructing is relatively expensive |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Wrong separators | Locale typo | Verify `navigator.language` |
| Currency code error | Bad ISO currency | Use valid `currency` |
| Hydration mismatch | Server locale ≠ client | Fix locale source of truth |
| Slow lists | New formatter per row | Reuse one instance |
| Sort “wrong” | Default `>` compare | Use `Collator` |

## Gotchas

> [!WARNING]
> **Filename typo** — API is `Intl`, not a separate “Formattor” package.

> [!WARNING]
> **Polyfills still needed on ancient engines** — check caniuse for `Segmenter` etc.

> [!WARNING]
> **Don’t parse with formatters** — formatting ≠ robust date parsing.

## When NOT to use

- **Timezone-heavy calendars** — consider Temporal / a date lib.
- **ICU message syntax apps** — FormatJS / bilingual message frameworks.
- **Pixel-perfect custom typography** — design system components wrapping Intl.

## Related

[[moment]] [[Packages]] [[LF and CRLF]]
