[[Descriptive/JavaScript/lexical analysis]] [[javascript]] [[Descriptive/Mermaid (DSL)]]

# Lexical Grammer

> *(Filename typo: **Grammar**)* — ECMAScript rules for how tokens combine into valid programs; pairs with [[lexical analysis]] scanning — **ECMA-262**.

## Mental model

**Lexical grammar** defines valid **tokens**. **Syntactic grammar** defines how tokens form statements and expressions. Two phases, one pipeline:

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

Grammar is **not** context-free for regex vs divide — parser uses lookahead.

## Standard config / commands

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

Parser must accept `?.`, `??`, `??=` as distinct tokens (ES2020+).

### Validate grammar in CI (esbuild fast check)

```bash
npx esbuild app.ts --bundle --outfile=/dev/null
# Syntax errors fail at parse — same grammar family as TS/JS
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Parse error on valid-looking code | Stage-3 syntax, old target | Update `ecmaVersion` / TS `target` |
| Regex literal fails | Flags or unescaped `/` | `new RegExp('pattern', 'u')` |
| Illegal return outside function | Script vs module top-level | Wrap in function or use module |
| `\u` in identifier wrong | Invalid escape in identifier | Use valid Unicode or ASCII |
| JSON.parse vs JS literal | JSON stricter grammar | Don't paste JS into JSON.parse |

## Gotchas

> [!WARNING]
> **Annex B (legacy web grammar)** allows some browser-only sloppy patterns (`<!--` as comment) — don't rely on them in modules or Node.

- **Grammar ≠ semantics:** `{}` is valid in object or block — parser role decides.
- **Shebang** is not in ECMA grammar text but universally stripped — see [[Descriptive/JavaScript/HashBang Comment]].
- **TypeScript** adds types erased before runtime — TS parser is superset grammar.

## When NOT to use

- Memorizing full ECMA BNF — use linter/parser errors and spec sections when debugging edge cases only.

## Related

[[Descriptive/JavaScript/lexical analysis]] [[javascript]] [[Descriptive/JavaScript/function]] [[compiler/library file]]
