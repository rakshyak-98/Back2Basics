[[Descriptive/JavaScript/Lexical Grammer]] [[javascript]] [[compiler/library file]] [[NodeJS/node command]] [[Descriptive/JavaScript/execution context]]

# Lexical analysis

> First compiler phase — scan source left-to-right into tokens; strip whitespace and comments — **ECMAScript lexical grammar**.

```txt
        Lexical analysis ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Lexer interviews cover tokenization before parse

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** Before parsing, the engine **tokenizes** source into atomic units: identifier…

```
"const x = 1 + 2;"
     │
     ▼ lexical analyzer (scanner)
- **Note:** [const] [Identifier(x)] [=] [Numeric(1)] [+] [Numeric(2)] [;]
     │
     ▼ parser
VariableDeclaration …
```

| Token class | Examples |
|-------------|----------|
| **Keyword** | `const`, `async`, `class` |
| **Identifier** | `foo`, `_private`, `$` |
| **Punctuator** | `{`, `}`, `=>`, `?.` |
| **String / Template** | `'a'`, `` `hi ${x}` `` |
| **Comment** | `//`, `/* */` — not tokens in output stream |

- **Note:** Invalid sequences (`@`, lone `#` in wrong place pre-private-fields) fail here…

## Technical Details
### Inspect tokens (Node — acorn/espree)

```javascript
import * as acorn from 'acorn';

const tokens = acorn.tokenizer('const x = 1;', { ecmaVersion: 'latest' });
for (let t = tokens(); t.type.name !== 'eof'; t = tokens()) {
  console.log(t.type.name, t.value ?? '');
}
```

### Line terminators (significant for ASI)

```javascript
return
  x; // ASI inserts ; after return → returns undefined

// Line terminators: \n, \r, \u2028, \u2029
```

### Hashbang handling

- `#!` on line 1 is treated as comment, stripped before tokenization

### Unicode identifiers

```javascript
const café = 1; // valid IdentifierName (Unicode ID_Start / ID_Continue)
```

## Mistakes to Avoid
> [!WARNING]
> **HTML `<script>`** parsing can treat `<!--` or `-->` as comment start in legacy browsers — avoid those sequences inside scripts in HTML.

- **Mistake:** **Strict mode** reserved words (`let`, `yield`) tokenize differe…
- **Mistake:** **JSON is not JS lexically**
- **Mistake:** **Minifiers** rename identifiers but must preserve token boundar…

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unexpected token` | Invalid char or future syntax | Match engine version; transpile |
| ASI surprise | newline after `return`, `throw`, `()` | Use semicolons or format with Prettier |
| Template literal parse error | Unclosed `` ` `` or `${` | Balance braces inside `${}` |
| Regex vs division ambiguity | `/` after expression | Wrap regex in parens or use `new RegExp` |
| Private field `#` error | Old parser | Target ES2022+ or avoid private fields |

## Pros/Cons or Trade-offs
- Don't hand-roll a lexer for production JS
- Runtime validation of user expressions
