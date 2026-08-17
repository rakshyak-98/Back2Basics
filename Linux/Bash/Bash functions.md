[[Bash syntax]] [[bash script]] [[Scripting]] [[bash sourcing other script]] [[bash flags]]

# Bash functions

> Bash functions are reusable shell blocks in the current session or a sourced file — they share the shell’s environment unless you isolate them.

```txt
        Bash functions ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows `local`, return codes, sourcing vs executing, and why `export -f` is ra…

## Sources
- [Bash Reference — Shell Functions](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html) — deep-dive
- [bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html) — overview

## Key Concepts
- **`local`:** Scope variables to the function.
- **`return` vs `exit`:** return leaves the function; exit leaves the shell/script.
- **Arguments:** `$1`…`$@` inside the function.
- **Sourcing:** Load a library of functions into the caller.
- **`export -f`:** Pass function to child bash — uncommon; prefer source.


- **Core:** A function is a named compound command. When defined in the current shell (or…

## Technical Details
```bash
#!/usr/bin/env bash
set -euo pipefail

greet() {
    local name="${1:-}"
    local age="${2:-}"

    if [[ -z "$name" ]]; then
        echo "Error: name required" >&2
        return 1
    fi

    echo "Hello, $name!"
    [[ -n "$age" ]] && echo "Age: $age"
}

greet "Alice" 30
greet "Bob" || echo "failed with $?"

export -f greet

log() {
    local level="$1"; shift
    echo "[$(date +%H:%M:%S)] [$level] $*" >&2
}

deploy() {
    local env="$1"
    log INFO "Deploying to $env"
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Function not found after script | Ran as `./` | `source` the file instead |
| Variable leak | Forgot `local` | Declare `local` |
| `exit` killed parent | Used exit in sourced fn | Prefer `return` |
| Broken under `sh` | Bash-only syntax | Use bash shebang |

## Mistakes to Avoid
- **Mistake:** Using `exit` inside sourced helper functions
- **Mistake:** Forgetting `local` and clobbering globals
- **Mistake:** Expecting `./lib.sh` to leave functions behind

## Pros/Cons or Trade-offs
- **Pro:** Structure scripts; reuse without forking.
- **Con:** Side effects on caller env if undisciplined.
- **Trade-off:** Functions in-shell vs external scripts for isolation.

## Comparison
- vs [[bash sourcing other script]]: how libraries get loaded


### Use cases
- Shared `log`/`die` helpers in deploy libraries, and wrapping SSH loops withou…
