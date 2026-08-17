[[Data structure]] [[DSA algorithms]] [[dsa problem solving Scaffold]]

# dsa modular arithmetics

> Modular arithmetic is math on remainders — wrap indices, hash, and contest math under a modulus.





## Interview Relevance
Modular arithmetic appears in hashing, wraparound indices, and contest math — wrong modulus handling fails edge cases.

## Sources
- [Wikipedia — Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic) — overview
- [CP-Algorithms — Modular arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) — deep-dive

## Key Concepts
```txt
(a + b) mod m = ((a mod m) + (b mod m)) mod m
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **mod** | Remainder | “Clock math.” |
| **Congruent** | Same remainder | `a ≡ b (mod m)` |
| **Inverse** | Multiply to 1 | “Exists if gcd(a,m)=1.” |
| **Wrap index** | Circular buffers | `(i+1) % n` |

## Technical Details
```js
const mod = (x, m) => ((x % m) + m) % m // positive remainder
const add = (a, b, m) => mod(a + b, m)
```

| Knob | Why it matters |
|------|----------------|
| Prime modulus | Inverses exist for all non-0 |
| BigInt | Avoid overflow in JS/Java |
| Order of ops | Overflow before mod lies |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Negative remainder | language `%` | Positive mod helper |
| Wrong contest answer | overflow | BigInt / long + mod |
| No inverse | gcd≠1 | Different modulus / method |
| Off-by-wrap | index -1 | `mod(i-1, n)` |

## Pros/Cons or Trade-offs
- **Trade-off:** Plain floats — rounding ≠ modular rings.
- **Trade-off:** Crypto without a library — don’t roll your own.

## Mistakes to Avoid
- Language `%` on negatives — JS/C differ in sign of remainder.
- **`(a*b)%m` with 32-bit ints** — multiply can overflow; cast wide first.
