[[compiler]] [[compile time]] [[Descriptive/JavaScript/Polyfilling]]

# Transpiler

> Source-to-source translator — rewrite modern (or alternate) syntax into another high-level dialect older runtimes or different platforms accept.

## Interview Relevance

Interviewers contrast transpile vs compile, why Babel/TypeScript exist, and the cost of source maps and downleveling for browser support matrices.

## Sources

- [Wikipedia — Source-to-source compiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) — overview
- [Babel — What is Babel](https://babeljs.io/docs/) — deep-dive

## Key Concepts

- **Source → source:** output remains a programming language humans/tools can read.
- **Downleveling:** ES202x → ES5, TypeScript → JavaScript, JSX → `React.createElement`.
- **Source maps:** map emitted lines back to original → debug the code you wrote.
- **Target matrix:** browsers/Node versions dictate which transforms and polyfills you need.

## Technical Details

```
Modern TS/JSX/ESNext ──transpile──► Plain JS ( + polyfills separately )
```

Examples: TypeScript compiler (`tsc`), Babel, Dart→JS (historical), CoffeeScript→JS, Java→Java (Android desugar-style tools).

| Concern | Handled by |
|---------|------------|
| Syntax transform | Transpiler |
| Missing runtime APIs | Polyfills / shims |
| Native machine code | Real [[compiler]] / JIT |

## Real-World Applications

Web apps ship transpiled bundles so one codebase runs on a support policy (e.g. “last two Chrome versions + defined Safari”).

**Example:** Optional chaining breaks an old WebView — lower `target` in Babel/`tsconfig` or drop that WebView from support.

## Pros/Cons or Trade-offs

- **Pro:** Use new language features without abandoning old runtimes on day one.
- **Con:** Build complexity, slower builds, and mismatches when source maps are missing.

## Comparison

- vs [[compiler]]: compilers typically emit machine code or VM bytecode; transpilers emit another high-level language.
- vs polyfill: transpile rewrites syntax; polyfill implements missing APIs at runtime.

## Mistakes to Avoid

- Transpiling syntax but forgetting polyfills for `Promise`, `fetch`, etc.
- Debugging minified output without source maps.
- Targeting “ESNext” in production with no defined browser policy.
