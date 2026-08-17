[[Data structure]] [[dsa intuition]] [[DSA algorithms]] [[algo/Two pointer]] [[sliding window]]

# dsa problem solving Scaffold

> A repeatable scaffold for review DSA — clarify, pattern-match, complexity, then code + tests.

```txt
        dsa problem solvin ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** A scaffold shows process maturity

## Sources
- [CTCI — process](https://www.crackingthecodinginterview.com/) — overview
- [MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive

## Key Concepts
```txt
- **Note:** 1 clarify I/O 2 examples 3 brute 4 pattern 5 code 6 test
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Constraints** | n, value ranges | “Pick O(n) vs O(n log n).” |
| **Brute force** | Correct slow | “Baseline before optimize.” |
| **Pattern** | two pointers / sliding… | “Name the tool.” |
| **Invariants** | What loop keeps true | “Explain why it works.” |

## Technical Details
```text
Ask: sorted? duplicates? in-place? mutable?
Examples: empty, one, two, duplicates, negatives
Complexity target from constraints (n=1e5 → ~O(n log n) max)
```

| Knob | Why it matters |
|------|----------------|
| Constraints | Kill impossible approaches early |
| Edge checklist | Empty/dupes/overflow |
| Speak invariants | Reviewer follows |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck coding | no brute first | Write slow correct |
| TLE | complexity vs n | Better pattern |
| WA | edges | empty/dupes/off-by-one |
| Can’t explain | no invariant | State loop promise |

## Mistakes to Avoid
- **Mistake:** Jumping to optimal
- **Mistake:** Silent assumptions — sorted input, unique keys, fit in int

## Pros/Cons or Trade-offs
- **Trade-off:** production bugfix with known root cause — scaffold is for unknown problems.
- **Trade-off:** Pure systems design — different checklist.
