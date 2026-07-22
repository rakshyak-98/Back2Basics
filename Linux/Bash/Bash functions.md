[[Bash syntax]] [[bash script]] [[Scripting]]

# Bash functions

> One-line: **Reusable shell blocks in the current session or sourced file** — share logic without fork/exec overhead of external scripts. Scope, `return`, and `local` prevent the subtle bugs that leak into prod deploy scripts.

## Mental model

Functions run in the **current shell** (no new process unless you call external commands). Variables are global by default — **`local` is mandatory** for parameters and temps. Exit status is `return N` (0–255) or last command's status. Functions are defined before use; order matters in sourced files.

```
source deploy.sh  →  functions loaded into shell
deploy_app        →  runs in same shell — can mutate cwd, env, exports
./deploy.sh       →  subshell (unless exec) — functions not retained
```

| vs | Function | Script |
|----|----------|--------|
| Process | same shell | usually subshell |
| Env/cwd side effects | yes | isolated if subshell |
| Speed | no fork for logic | fork per invocation |
| Shebang | N/A | `#!/usr/bin/env bash` |

## Standard config / commands

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

# Usage
greet "Alice" 30
greet "Bob" || echo "failed with $?"

# Export for subshells (rare — prefer sourcing)
export -f greet

# Recursive / nested
log() {
    local level="$1"; shift
    echo "[$(date +%H:%M:%S)] [$level] $*" >&2
}

deploy() {
    local env="$1"
    log INFO "Deploying to $env"
    # ...
}
```

**Pass arrays (bash 4+):**

```bash
run_on_hosts() {
    local -a hosts=("$@")
    local h
    for h in "${hosts[@]}"; do
        ssh "$h" "$@"
    done
}
```

**Cleanup pattern:**

```bash
cleanup() {
    local rc=$?
    rm -f /tmp/work.$$
    exit "$rc"
}
trap cleanup EXIT
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `command not found` for function | Defined after call | Reorder; source lib first |
| Variable clobbered global | Missing `local` | Add `local` to all params/temps |
| `return: can only return from function` | return in sourced top-level | Use `exit` in scripts, `return` in functions only |
| Function not in cron | Cron minimal env | Full path; source profile; absolute paths |
| `set -e` exits unexpectedly | Failing cmd in function | `|| true` or explicit handling |
| Export -f fails | Non-bash shell | Force bash in shebang |

## Gotchas

> [!WARNING]
> **Functions + `set -e`** — failure inside function may not exit caller unless `set -e` and caller invokes directly. Test failure paths.

> [!WARNING]
> **Naming collision** — function `ls` shadows binary. Prefix with `_` or namespace (`app::deploy` as name with colon).

- **Recursive functions** — bash has no tail-call optimization; deep recursion blows stack.
- **`$*` vs `$@`** — use `"$@"` for preserved word splitting on args.

## When NOT to use

- **Complex CLI with flags** — standalone script or proper language (Python/Go).
- **sudo boundaries** — function runs as current user; can't elevate inside without sudo in body.
- **Library for multiple shells** — POSIX `sh` functions differ; use external script.

## Related

[[Bash syntax]] [[bash script]] [[Scripting]] [[bash sourcing other script]]
