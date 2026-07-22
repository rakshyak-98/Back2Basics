[[bash script]] [[Bash syntax]] [[Bash functions]] [[Scripting]]

# Bash sourcing other scripts

> One-line: **`source` / `.` loads a script into the current shell** — libraries, env, and functions without a fork. Wrong path resolution breaks cron, systemd, and CI the moment cwd changes.

## Mental model

**Sourcing** executes commands in the **current shell context**. Exported vars, functions, and `cd` persist. **Executing** `./script.sh` runs a subshell (usually) — isolation unless script mutates parent via exports you re-import.

```
. lib/utils.sh   →  functions available immediately
./lib/utils.sh   →  subshell; functions gone when script ends
```

| Pattern | Use |
|---------|-----|
| `source file` | bash builtin — readable |
| `. file` | POSIX equivalent |
| `${BASH_SOURCE[0]}` | Path of file being sourced — anchor relative imports |

**Critical:** always resolve paths relative to **the sourced file**, not `$PWD`.

## Standard config / commands

**Safe library load (production pattern):**

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

# Now call functions from utils.sh
deploy_app staging
```

**utils.sh (sourced library):**

```bash
# lib/utils.sh — no shebang required; no exit unless fatal
deploy_app() {
    local env="${1:?env required}"
    echo "Deploying to $env"
}
```

**Optional config overlay:**

```bash
CONFIG="${CONFIG:-/etc/myapp/config.sh}"
[[ -f "$CONFIG" ]] && source "$CONFIG"
```

**systemd ExecStartPre sourcing env:**

```ini
[Service]
EnvironmentFile=-/etc/default/myapp
ExecStart=/opt/myapp/bin/run.sh
```

Prefer `EnvironmentFile=` over sourcing in wrapper when possible — clearer permissions.

**Avoid:**

```bash
source ./lib/utils.sh      # breaks when cwd != script dir
source ~/lib/utils.sh      # breaks for other users/CI
. /etc/profile             # pulls login side effects; non-reproducible
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `No such file` on source | Relative to cwd | Use `BASH_SOURCE[0]` dirname pattern |
| Works interactive, fails cron | Minimal PATH/cwd | Absolute paths; set PATH in script |
| `set -u` unbound variable | Order of source | Define defaults before source or in library |
| Double-sourced side effects | Guard with variable | `[[ -n "${_LIB_LOADED:-}" ]] && return; _LIB_LOADED=1` |
| Function not found | Sourced subshell by mistake | Use `source` not `./` |
| Permission denied | File not readable | chmod 644; check AppArmor |

**Idempotent library guard:**

```bash
# lib/utils.sh top
[[ -n "${_UTILS_SH_LOADED:-}" ]] && return 0
_UTILS_SH_LOADED=1
```

## Gotchas

> [!WARNING]
> **Sourcing untrusted scripts** — equivalent to running arbitrary code in your shell. Same trust as `curl | bash`.

> [!WARNING]
> **`exit` in sourced file** — kills parent script/shell. Libraries should `return` (only valid inside sourced context or functions).

- **shellcheck `SC1090/1091`** — dynamic source path; annotate or structure known paths.
- **Symlinks** — `BASH_SOURCE` vs `readlink -f` for real path when symlinks involved.

## When NOT to use

- **Large standalone job** — executable script with shebang + `main "$@"`.
- **Cross-language reuse** — Python/Go module, not bash source.
- **Secrets in sourced file** — world-readable `/etc/default` leaks; use restricted permissions + systemd credentials.

## Related

[[bash script]] [[Bash syntax]] [[Bash functions]] [[Scripting]]
