[[JavaScript]]

# pre-parser

> One-line: what / why for **pre-parser** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- also known as the initial phase of parsing.
- identifies and handles certain language constructs before the full parsing process begins.
- help in detecting and reporting syntax errors early in the compilation process.
- handling directives ("use strict") are processed during this phase to enable strict mode.
- function declarations are hoisted, processed before the actual parsing takes place.
- other pre processing tasks like handling line terminators, recognizing regular expression, and detecting template literals.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
