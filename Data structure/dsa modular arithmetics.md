[[Data structure]] [[DSA algorithms]]

# dsa modular arithmetics

> Modular arithmetic is math on remainders — wrap indices, hash, and contest math under a modulus.

## Mental model

**Say it in one breath:** Work mod `m` so values stay in `0…m-1`; watch negative mods and overflow before `%`.

```txt
(a + b) mod m = ((a mod m) + (b mod m)) mod m
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **mod** | Remainder | “Clock math.” |
| --- | --- | --- |
| **Congruent** | Same remainder | `a ≡ b (mod m)` |
| **Inverse** | Multiply to 1 | “Exists if gcd(a,m)=1.” |
| **Wrap index** | Circular buffers | `(i+1) % n` |

## Standard config / commands

```js
const mod = (x, m) => ((x % m) + m) % m // positive remainder
const add = (a, b, m) => mod(a + b, m)
```

| Knob | Why it matters |

| Prime modulus | Inverses exist for all non-0 |
| --- | --- |
| BigInt | Avoid overflow in JS/Java |
| Order of ops | Overflow before mod lies |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Negative remainder | language `%` | Positive mod helper |
| Wrong contest answer | overflow | BigInt / long + mod |
| No inverse | gcd≠1 | Different modulus / method |
| Off-by-wrap | index -1 | `mod(i-1, n)` |

## Gotchas

> [!WARNING]
> **Language `%` on negatives** — JS/C differ in sign of remainder.

> [!WARNING]
> **`(a*b)%m` with 32-bit ints** — multiply can overflow; cast wide first.

## When NOT to use

- **Plain floats** — rounding ≠ modular rings.
- **Crypto without a library** — don’t roll your own.

## Related

[[DSA algorithms]] [[dsa problem solving Scaffold]]
