[[Bash]] [[bash script]] [[CLI]] [[Commands]] [[bash flags]] [[Bash syntax]]

# Scripting

> Shell scripting automates repeatable operator work — compose POSIX/Bash builtins and core utilities with explicit error handling.





## Interview Relevance
Shows discipline: `set -euo pipefail`, quoting, when to leave Bash for Python/jq — not clever one-liners that break on spaces.

## Sources
- [Bash Reference Manual — GNU](https://www.gnu.org/software/bash/manual/bash.html) — deep-dive
- [bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html) — deep-dive

## Core Definition
Bash scripts glue [[Commands]] into pipelines. Prefer small scripts with `set -euo pipefail` ([[bash flags]]), quoted variables ([[Bash syntax]]), and functions ([[Bash functions]]) over sprawling one-liners.

## Key Concepts
- **Shebang:** `#!/usr/bin/env bash` vs `#!/bin/sh` — Bashisms fail under dash/`sh`.
- **Strict mode:** `-e` exit on error, `-u` unset vars, `-o pipefail` pipeline failures.
- **Quoting:** `"$var"` prevents word-splitting and globbing.
- **Functions + main:** Structure for testability and clearer `$@` handling.
- **Exit codes:** Non-zero means failure for automation and CI.

## Technical Details
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

main() {
  local target="${1:?usage: $0 <dir>}"
  find "$target" -type f -name '*.log' -mtime +7 -delete
}

main "$@"
```

```bash
bash -x script.sh          # trace every command
shellcheck script.sh       # static analysis (if installed)
```

| Task | Better tool |
|------|-------------|
| JSON / API parsing | Python, [[jq]] |
| Complex text columns | [[awk]], Python |
| Long-running services | [[services/systemd]] unit, not a while-true loop |
| Cross-platform | Python with explicit dependencies |

| Failure | Fix |
|---------|-----|
| Silent continue after error | Add `set -e` or check `$?` |
| Word splitting on `$var` | Quote: `"$var"` |
| Wrong interpreter | Avoid Bashisms in `/bin/sh` |

## Real-World Applications
Deploy hooks, log cleanup cron wrappers, and incident “runbook scripts” that must fail loudly when a step fails.

## Pros/Cons or Trade-offs
- **Pro:** Instant on every Linux box; great for glue.
- **Con:** Weak typing, fragile parsing, poor for complex state.
- **Trade-off:** Short Bash + strong tools beats a 500-line Bash “program.”

## Comparison
vs interactive shell: scripts need strict mode and explicit paths. vs Python: use Python when data structures or HTTP dominate. Related: [[bash script]], [[bash sourcing other script]].

## Mistakes to Avoid
- Unquoted variables around paths and `rm`.
- Relying on `cd` relative state in cron without absolute paths.
- Shipping Bash-only syntax with a `#!/bin/sh` shebang.
