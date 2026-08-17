[[Descriptive/JavaScript/lexical analysis]] [[javascript]] [[Descriptive/Mermaid (DSL)]] [[Descriptive/JavaScript/function]] [[compiler/library file]]

# Lexical Grammer

> *(Filename typo: **Grammar**)* — ECMAScript rules for how tokens combine into valid programs; pairs with [[lexical analysis]] scanning — **ECMA-262**.

```txt
        Lexical Grammer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Lexical grammar questions check how JS source is tokenized

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** **Lexical grammar** defines valid **tokens**

```
Source text
    → [[lexical analysis]] (tokens)
    → syntactic parse (AST)
    → execution
```

Key lexical rules engineers hit daily:

| Rule | Effect |
|------|--------|
| **InputElement** | Token, comment, or whitespace |
| **LineTerminator** | Triggers ASI between statements |
| **StringLiteral** | `'`, `"`, or template `` ` `` |
| **NumericLiteral** | Decimal, hex `0x`, binary `0b`, BigInt `n` |
| **RegularExpressionLiteral** | Context-sensitive — parser disambiguates `/` |

- **Note:** Grammar is **not** context-free for regex versus divide

## Technical Details
### ASI (automatic semicolon insertion) — grammar + line terminators

```javascript
const a = 1
const b = 2        // OK — ASI inserts ; after 1

;(function () {}) // leading ; guards against previous line concat
```

### Template literal grammar

```javascript
const tag = (strings, ...values) => strings.raw[0];
tag`line1\n`; // raw newline in raw property
```

### Optional chaining & nullish — modern punctuators

```javascript
obj?.prop ?? defaultValue;
```

- Parser must accept `?.`, `??`, `??=` as distinct tokens (ES2020+).

### Validate grammar in CI (esbuild fast check)

```bash
npx esbuild app.ts --bundle --outfile=/dev/null
# Syntax errors fail at parse — same grammar family as TS/JS
```

## Mistakes to Avoid
> [!WARNING]
> **Annex B (legacy web grammar)** allows some browser-only sloppy patterns (`<!--` as comment) — don't rely on them in modules or Node.

- **Mistake:** **Grammar ≠ semantics:** `{}` is valid in object or block
- **Mistake:** **Shebang** is not in ECMA grammar text but universally stripped
- **Mistake:** **TypeScript** adds types erased before runtime

| Symptom | Check | Fix |
|---------|-------|-----|
| Parse error on valid-looking code | Stage-3 syntax, old target | Update `ecmaVersion` / TS `target` |
| Regex literal fails | Flags or unescaped `/` | `new RegExp('pattern', 'u')` |
| Illegal return outside function | Script vs module top-level | Wrap in function or use module |
| `\u` in identifier wrong | Invalid escape in identifier | Use valid Unicode or ASCII |
| JSON.parse vs JS literal | JSON stricter grammar | Don't paste JS into JSON.parse |

## Pros/Cons or Trade-offs
- Memorizing full ECMA BNF
