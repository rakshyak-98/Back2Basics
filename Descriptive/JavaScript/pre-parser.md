[[Javascript]] [[JavaScript/lexical analysis]] [[JavaScript/Lexical Grammer]]

# pre-parser

> Engines skim source before full parse — find functions/boundaries early for faster startup and lazy compile.

---

## Mental model

**Say it in one breath:** Pre-parse/lazy parse builds a light view of the script; full parse/compile waits until a function runs (engine-specific).

```txt
scan → pre-parse (lazy) → full parse on first run → execute
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Lazy parse** | Defer full AST | “Faster cold start.” |
| **Eager parse** | Parse now | “Directives / certain patterns.” |
| **Syntax error** | Still caught | “Pre-parse must see structure.” |
| **vs transpile** | Build-time | “Babel isn’t the engine pre-parser.” |

---

## Standard config / commands

```js
// practical: keep top-level light; put heavy code in functions
export function rarelyUsed() { /* parsed when called (often) */ }
```

| Knob | Why it matters |
|------|----------------|
| Bundle splitting | Less source at startup |
| Top-level work | Runs (and parses) eagerly |
| Eval/new Function | Often forces eager paths |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow startup | huge top-level | Code-split; defer |
| Surprise syntax error late | lazy path | CI parse (`tsc`/lint) |
| Eval cost | dynamic code | Avoid eval |

---

## Gotchas

> [!WARNING]
> **Engine heuristics change** — don’t depend on lazy parse for correctness.

> [!WARNING]
> **Build tools ≠ VM pre-parse** — still ship less JS.

---

## When NOT to use

- **Correctness reasoning** — assume full parse in CI.
- **Micro-optimizing parse** — measure; bundling usually dominates.

## Related

[[JavaScript/lexical analysis]] [[JavaScript/Call stack]]
