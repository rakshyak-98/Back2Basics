[[javascript]]

# IIFC

> One-line: what / why for **IIFC** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Immediate Invoked Function Call
- it helps you wrap an amount of work your want to do without leaving any global variables behind.
- use the scope of the immediate function to privately store some data, specific to the inner function you return.
- can be used when you define object properties.
	- property that will never change during the life of the object, before you define it a bit of work is needed.
> [!INFO] The semicolon (`;`) before an **Immediately Invoked Function Expression (IIFE)** in JavaScript is used to **prevent syntax errors** when the preceding code does not end properly with a semicolon.

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
