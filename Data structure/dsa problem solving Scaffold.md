[[Data structure]] [[dsa intuition]] [[DSA algorithms]]

# dsa problem solving Scaffold

> A repeatable scaffold for interview DSA — clarify, pattern-match, complexity, then code + tests.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Restate → examples → brute force → improve with a pattern → complexity → code edge cases.

```txt
1 clarify I/O  2 examples  3 brute  4 pattern  5 code  6 test
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Constraints** | n, value ranges | “Pick O(n) vs O(n log n).” |
| **Brute force** | Correct slow | “Baseline before optimize.” |
| **Pattern** | two pointers / sliding… | “Name the tool.” |
| **Invariants** | What loop keeps true | “Explain why it works.” |

---

## Standard config / commands

```text
Ask: sorted? duplicates? in-place? mutable?
Examples: empty, one, two, duplicates, negatives
Complexity target from constraints (n=1e5 → ~O(n log n) max)
```

| Knob | Why it matters |
|------|----------------|
| Constraints | Kill impossible approaches early |
| Edge checklist | Empty/dupes/overflow |
| Speak invariants | Interviewer follows |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck coding | no brute first | Write slow correct |
| TLE | complexity vs n | Better pattern |
| WA | edges | empty/dupes/off-by-one |
| Can’t explain | no invariant | State loop promise |

---

## Gotchas

> [!WARNING]
> **Jumping to optimal** — if you can’t prove it, start brute and optimize.

> [!WARNING]
> **Silent assumptions** — sorted input, unique keys, fit in int.

---

## When NOT to use

- **production bugfix with known root cause** — scaffold is for unknown problems.
- **Pure systems design** — different checklist.

## Related

[[dsa intuition]] [[algo/Two pointer]] [[sliding window]] [[DSA algorithms]]
