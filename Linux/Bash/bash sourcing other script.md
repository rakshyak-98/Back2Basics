[[bash script]] [[Bash syntax]] [[Bash functions]] [[Scripting]] [[bash flags]]

# Bash sourcing other scripts

> Sourcing runs another file in the current shell — functions, variables, and cd persist; executing `./script.sh` usually does not.

```txt
        Bash sourcing othe ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic trap: `source` vs execute, `BASH_SOURCE` for library paths, and never…

## Sources
- [Bash Reference — Bourne Shell Builtins (`.` / `source`)](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html) — deep-dive
- [BashFAQ — sourcing](https://mywiki.wooledge.org/BashFAQ/028) — overview

## Key Concepts
- **Same shell:** Exports, functions, `cd`, options affect the caller.
- **Library pattern:** `source "$(dirname …)/lib/utils.sh"`.
- **`BASH_SOURCE`:** Reliable path to the current script file.
- **`return` in sourced file:** Leaves the sourced file, not always the whole script.
- **`exit` in sourced file:** Exits the caller shell/script.


- **Core:** `. file` or `source file` reads and executes commands in the **current** shel…

## Technical Details
```txt
. lib/utils.sh   →  functions available immediately
./lib/utils.sh   →  subshell; functions gone when script ends
```

```bash
#!/usr/bin/env bash
set -euo pipefail

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib"

if [[ -f "$_LIB_DIR/utils.sh" ]]; then
    # shellcheck source=/dev/null
    source "$_LIB_DIR/utils.sh"
else
    echo "Error: utils.sh not found in $_LIB_DIR" >&2
    exit 1
fi

deploy_app staging
```

```bash
# lib/utils.sh — no shebang required; prefer return over exit
deploy_app() {
    local env="${1:?env required}"
    echo "Deploying to $env"
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| function: not found | Used `./lib` | `source` instead |
| Caller died unexpectedly | `exit` in library | Use `return` |
| Wrong lib path | cwd-relative source | Resolve via `BASH_SOURCE` |
| set -e quirks | options inherited | Document; isolate with subshell if needed |

## Mistakes to Avoid
- **Mistake:** Sourcing with relative paths that break when cwd changes
- **Mistake:** Putting `exit 1` in helpers meant to be sourced
- **Mistake:** Assuming `./utils.sh` loads functions into the parent shell

## Pros/Cons or Trade-offs
- **Pro:** Zero-fork reuse; true shared state when wanted.
- **Con:** Pollution and accidental `exit`; harder to reason about than pure functions in a language.
- **Trade-off:** Source libraries vs `bash -c` / external scripts for isolation.

## Comparison
- vs executing a script: isolation vs shared env


### Use cases
- Shared deploy helpers (`log`, `die`, `require_env`) across multiple scripts, …
