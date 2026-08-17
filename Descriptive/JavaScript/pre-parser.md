[[Javascript]] [[JavaScript/lexical analysis]] [[JavaScript/Lexical Grammer]] [[JavaScript/Call stack]]

# pre-parser

> Engines skim source before full parse — find functions/boundaries early for faster startup and lazy compile.

```txt
        pre-parser ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Pre-parser questions check lazy parsing optimizations in engines

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
scan → pre-parse (lazy) → full parse on first run → execute
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Lazy parse** | Defer full AST | “Faster cold start.” |
| **Eager parse** | Parse now | “Directives / certain patterns.” |
| **Syntax error** | Still caught | “Pre-parse must see structure.” |
| **vs transpile** | Build-time | “Babel isn’t the engine pre-parser.” |

## Technical Details
```js
// practical: keep top-level light; put heavy code in functions
export function rarelyUsed() { /* parsed when called (often) */ }
```

| Knob | Why it matters |
|------|----------------|
| Bundle splitting | Less source at startup |
| Top-level work | Runs (and parses) eagerly |
| Eval/new Function | Often forces eager paths |

## Mistakes to Avoid
> [!WARNING]
> **Engine heuristics change** — don’t depend on lazy parse for correctness.

> [!WARNING]
> **Build tools ≠ VM pre-parse** — still ship less JS.

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow startup | huge top-level | Code-split; defer |
| Surprise syntax error late | lazy path | CI parse (`tsc`/lint) |
| Eval cost | dynamic code | Avoid eval |

## Pros/Cons or Trade-offs
- **Correctness reasoning** — assume full parse in CI.
- **Micro-optimizing parse** — measure; bundling usually dominates.
