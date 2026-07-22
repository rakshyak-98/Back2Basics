[[bash script]] [[CLI]] [[Bash syntax]] [[Bash functions]]

# Scripting

> One-line: glue Unix tools and business logic with **shell scripts** — automation, cron wrappers, deploy hooks, and incident one-offs. **Know when bash stops and Python starts.**

## Mental model

A shell script is a sequence of commands run by an interpreter (`bash`, `sh`). The shell expands variables, splits words, runs pipelines, and returns an **exit code** the next command (or CI) can test. Scripts inherit environment from parent; they don't magically load your interactive `.bashrc` unless sourced.

```
#!/bin/bash
set -euo pipefail
        │
        ├── -e  exit on first failure
        ├── -u  error on unset variables
        └── pipefail  pipe fails if any stage fails
```

| Use shell for | Use Python/Go for |
|---------------|-------------------|
| Wrapping CLI tools | Complex data structures |
| Cron/systemd hooks | APIs, JSON parsing at scale |
| Deploy rsync/tar glue | Libraries, test suites |
| Quick incident fixes | Anything > ~200 lines |

## Standard config / commands

**Minimal production template:**

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG="${SCRIPT_DIR}/run.log"

log() { printf '[%s] %s\n' "$(date -Iseconds)" "$*" | tee -a "$LOG"; }

main() {
  log "starting"
  # work here
  log "done"
}

main "$@"
```

**Variables & arguments:**

```bash
name="World"
count=42
echo "Hello, $name"

# Positional args
echo "Script: $0"
echo "First arg: ${1:-default}"    # default if unset
echo "All args: $*"

# Read loop
while IFS= read -r line; do
  echo "$line"
done < /etc/hosts
```

**Conditionals & tests:**

```bash
if [[ -f /etc/app.conf ]]; then
  source /etc/app.conf
fi

if [[ "$ENV" == "prod" ]]; then
  set -x                            # trace — remove after debug
fi

# Numeric / string
[[ $count -gt 10 ]]
[[ "$user" == "root" ]]
```

**Functions & exit codes:**

```bash
backup() {
  local src=$1 dst=$2
  rsync -a "$src/" "$dst/"
}

if backup /data /backup; then
  echo ok
else
  echo "backup failed: $?" >&2
  exit 1
fi
```

**Common patterns:**

```bash
# Temp file safe cleanup
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# Idempotent mkdir
mkdir -p /var/lib/myapp

# Retry loop
for i in {1..5}; do
  curl -sf http://localhost/health && break
  sleep 2
done

# Parallel (careful with load)
printf '%s\n' host1 host2 | xargs -P4 -I{} ssh {} 'uptime'
```

**Make executable & run:**

```bash
chmod +x deploy.sh
./deploy.sh
# or explicit interpreter
bash deploy.sh
```

See [[bash script]] for deeper syntax; [[crontab]] and [[systemd]] for scheduling.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `bad interpreter` | Shebang path wrong | `#!/usr/bin/env bash`; `which bash` |
| Works manually, fails in cron | PATH, cwd, env | Absolute paths; `cd` in script; log env |
| `set -u` unbound variable | Typo or optional arg | `${var:-default}`; validate `$#` |
| Silent failure in pipe | Missing `pipefail` | `set -o pipefail` |
| Word-splitting bug | Unquoted `$var` | Quote: `"$var"`; arrays for lists |
| Infinite loop | `while true` without break | Add timeout; log iteration |

## Gotchas

> [!WARNING]
> **`sh` vs `bash`** — Debian `/bin/sh` is dash; bashisms `[[ ]]`, `{1..10}` fail. Shebang `bash` if you need bash.

> [!WARNING]
> **Sourcing vs executing** — `source script.sh` runs in current shell (can overwrite cwd/env); `./script.sh` subshell.

> [!WARNING]
> **Parsing JSON/YAML in bash** — fragile. Use `jq`/`yq` or Python for non-trivial structure.

> [!WARNING]
> **Secrets in scripts** — world-readable `chmod 755` script with API key. Use env from systemd/cron, mode 600 files, vault.

## When NOT to use

- **Complex application logic** → Python, Go, Node.
- **Cross-platform GUI** → not shell.
- **Long-running services** → [[systemd]] unit + proper binary, not while-true bash.
- **Concurrency-heavy** → language with real threading/async.

## Related

[[bash script]] [[CLI]] [[Bash syntax]] [[Bash functions]] [[crontab]] [[systemd]] [[grep]] [[awk]]
