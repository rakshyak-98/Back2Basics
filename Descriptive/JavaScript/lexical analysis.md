[[Descriptive/JavaScript/Lexical Grammer]] [[javascript]] [[compiler/library file]] [[NodeJS/node command]]

# Lexical analysis

> First compiler phase — scan source left-to-right into tokens; strip whitespace and comments — **ECMAScript lexical grammar**.

## Mental model

Before parsing, the engine **tokenizes** source into atomic units: identifiers, keywords, numbers, strings, operators, punctuators. Insignificant input (spaces, comments, line terminators) is discarded or used only for ASI (automatic semicolon insertion).

```
"const x = 1 + 2;"
     │
     ▼ lexical analyzer (scanner)
[const] [Identifier(x)] [=] [Numeric(1)] [+] [Numeric(2)] [;]
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

Invalid sequences (`@`, lone `#` in wrong place pre-private-fields) fail here with **SyntaxError** before execution.

## Standard config / commands

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

`#!` on line 1 is treated as comment, stripped before tokenization — see [[Descriptive/JavaScript/HashBang Comment]].

### Unicode identifiers

```javascript
const café = 1; // valid IdentifierName (Unicode ID_Start / ID_Continue)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unexpected token` | Invalid char or future syntax | Match engine version; transpile |
| ASI surprise | newline after `return`, `throw`, `()` | Use semicolons or format with Prettier |
| Template literal parse error | Unclosed `` ` `` or `${` | Balance braces inside `${}` |
| Regex vs division ambiguity | `/` after expression | Wrap regex in parens or use `new RegExp` |
| Private field `#` error | Old parser | Target ES2022+ or avoid private fields |

## Gotchas

> [!WARNING]
> **HTML `<script>`** parsing can treat `<!--` or `-->` as comment start in legacy browsers — avoid those sequences inside scripts in HTML.

- **Strict mode** reserved words (`let`, `yield`) tokenize differently in sloppy vs module code.
- **JSON is not JS lexically** — no comments, trailing commas, unquoted keys.
- **Minifiers** rename identifiers but must preserve token boundaries — broken source maps show lexical phase errors as wrong lines.

## When NOT to use

- Don't hand-roll a lexer for production JS — use established parser (Babel, TypeScript, acorn).
- Runtime validation of user expressions — parse in sandbox, never `eval` unchecked.

## Related

[[Descriptive/JavaScript/Lexical Grammer]] [[Descriptive/JavaScript/execution context]] [[javascript]] [[compiler/library file]]
