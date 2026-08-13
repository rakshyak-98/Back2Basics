[[Bash]] [[bash script]] [[CLI]] [[Commands]]

# Scripting

> Shell scripting automates repeatable operator work — compose POSIX/Bash builtins and core utilities with explicit error handling.

Bash scripts glue [[Commands]] into pipelines. Prefer small scripts with `set -euo pipefail` ([[bash flags]]), quoted variables ([[Bash syntax]]), and functions ([[Bash functions]]) over sprawling one-liners.

## Minimal robust template

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

## When to leave Bash

| Task | Better tool |
|------|-------------|
| JSON / API parsing | Python, [[jq]] |
| Complex text columns | [[awk]], Python |
| Long-running services | [[systemd]] unit, not a while-true loop |
| Cross-platform | Python with explicit dependencies |

## Debugging scripts

```bash
bash -x script.sh          # trace every command
shellcheck script.sh       # static analysis (if installed)
```

| Failure | Fix |
|---------|-----|
| Silent continue after error | Add `set -e` or check `$?` |
| Word splitting on `$var` | Quote: `"$var"` |
| Wrong interpreter | `#!/bin/bash` vs `#!/bin/sh` — avoid Bashisms in `/bin/sh` |

## Related

[[bash script]] · [[bash sourcing other script]] · [[Bash syntax]] · [[bash flags]]

## Sources

- [Bash Reference Manual — GNU](https://www.gnu.org/software/bash/manual/bash.html)
- `man 1 bash`
