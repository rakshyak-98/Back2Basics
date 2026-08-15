[[Security]] [[C]] [[gcc]] [[Makefile]]

# Preprocessor

> Text transform before the real compiler: macros, includes, and conditional compilation (`#define`, `#include`, `#ifdef`).

## Interview Relevance

Systems/C interviews: what happens before compilation — macros, includes, conditional compilation — and macro footguns.

## Sources

- [GCC — The C Preprocessor](https://gcc.gnu.org/onlinedocs/cpp/) — deep-dive
- [Wikipedia — Preprocessor](https://en.wikipedia.org/wiki/Preprocessor) — overview

## Core Definition

A preprocessor rewrites source text before the compiler proper — in C/C++: `#include`, `#define` macros, and `#ifdef` conditionals.

## Key Concepts

```txt
source.c ──#include / #define / #if──► preprocessed.c ──► compile
```

| Tool | Job |
|------|-----|
| **Lexical preprocessor** | Token paste/substitution (C preprocessor) |
| **Lexer / tokenizer** | Split text into identifiers, operators, literals |
| **Parser** | Build AST from tokens |

## Technical Details

```bash
# See what the compiler actually compiles
gcc -E main.c -o main.i
clang -E -dM main.c          # dump macros
cpp -I./include main.c
```

```c
#include "config.h"
#ifdef DEBUG
  #define LOG(...) fprintf(stderr, __VA_ARGS__)
#else
  #define LOG(...)
#endif
```

| Knob | Why it matters |
|------|----------------|
| `-I` paths | Missing headers → expand fail |
| `#pragma once` / include guards | Duplicate symbol / redefinition |
| `-DFOO=1` | Define from CLI / build system |

### Lexical preprocessors

Lowest level: operate on tokens before parsing — substitute token sequences per user rules (`#define`, macros).

### Lexical tokenization

Split text into lexemes (identifiers, operators, punctuation, literals). Stages: **scan** (segment) → **evaluate** (turn lexemes into values). Used by compilers, linters, pretty-printers.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `No such file or directory` include | `-I` / wrong quotes | Fix path; `"local"` vs `<system>` |
| Mysterious expanded code | Macro side effects | `gcc -E`; prefer inline functions |
| Redefinition errors | Double include | Include guards / `#pragma once` |
| `#ifdef` branch wrong | `-D` flags in build | Print `clang -E -dM`; align CMake/Make |
| Pasting errors `##` | Invalid token paste | Fix macro; avoid complex `##` |

## Real-World Applications

Debug macro expansion with `gcc -E` when a `#define` changes types or includes the wrong header.

## Pros/Cons or Trade-offs

- **Pro:** Cheap compile-time configuration and header composition in C/C++.
- **Con:** Business logic configuration — use real configuration languages, not `#ifdef` forests.
- **Con:** New languages with modules — rely on the module system instead of include soup.
- **Con:** Security policy — preprocessor can’t enforce runtime authz.

## Comparison

- vs compiler proper: preprocessor is text rewrite before parsing/typing.
- vs lexer: lexical analysis tokenizes; C preprocessor runs earlier on source text.

## Mistakes to Avoid

- Macros don’t respect types or scopes — prefer `static inline` / `constexpr` in C++.
- Multi-eval arguments — `MAX(++i, a)` can increment twice; use functions.
- Huge `-E` output — includes expand everything; don’t commit preprocessed files.
