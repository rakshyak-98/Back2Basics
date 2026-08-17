[[Security]] [[C]] [[gcc]] [[Makefile]]

# Preprocessor

> Text transform before the real compiler: macros, includes, and conditional compilation (`#define`, `#include`, `#ifdef`).

```txt
        Preprocessor ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Systems/C interviews: what happens before compilation

## Sources
- [GCC — The C Preprocessor](https://gcc.gnu.org/onlinedocs/cpp/) — deep-dive
- [Wikipedia — Preprocessor](https://en.wikipedia.org/wiki/Preprocessor) — overview

## Key Concepts
```txt
- **Note:** source.c ──#include / #define / #if──► preprocessed.c ──► compile
```

| Tool | Job |
|------|-----|
| **Lexical preprocessor** | Token paste/substitution (C preprocessor) |
| **Lexer / tokenizer** | Split text into identifiers, operators, literals |
| **Parser** | Build AST from tokens |


- **Core:** A preprocessor rewrites source text before the compiler proper

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

- Lowest level: operate on tokens before parsing

### Lexical tokenization

- Split text into lexemes (identifiers, operators, punctuation, literals).
- Stages: **scan** (segment) → **evaluate** (turn lexemes into values).
- Used by compilers, linters, pretty-printers.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `No such file or directory` include | `-I` / wrong quotes | Fix path; `"local"` vs `<system>` |
| Mysterious expanded code | Macro side effects | `gcc -E`; prefer inline functions |
| Redefinition errors | Double include | Include guards / `#pragma once` |
| `#ifdef` branch wrong | `-D` flags in build | Print `clang -E -dM`; align CMake/Make |
| Pasting errors `##` | Invalid token paste | Fix macro; avoid complex `##` |

## Mistakes to Avoid
- **Mistake:** Macros don’t respect types or scopes
- **Mistake:** Multi-eval arguments
- **Mistake:** Huge `-E` output

## Pros/Cons or Trade-offs
- **Pro:** Cheap compile-time configuration and header composition in C/C++.
- **Con:** Business logic configuration — use real configuration languages, not `#ifdef` forests.
- **Con:** New languages with modules — rely on the module system instead of include soup.
- **Con:** Security policy — preprocessor can’t enforce runtime authz.

## Comparison
- vs compiler proper: preprocessor is text rewrite before parsing/typing.
- vs lexer: lexical analysis tokenizes; C preprocessor runs earlier on source text.


### Use cases
- Debug macro expansion with `gcc -E` when a `#define` changes types or include…
