[[Linux/Bash/Bash functions]] [[Linux/Scripting]] [[Linux/commands/common commands]]

# Unbound variable (bash `set -u`)

> Referencing an unset shell variable is an error when `set -u` (nounset) is on — catches typos before prod scripts half-run.

## Mental model

Default bash expands unset vars to empty string — silent bugs (`rm -rf $DIR/` with empty DIR). **`set -u`** (or `set -o nounset`) aborts on unbound expansion. Often paired with **`set -e`** (errexit) and **`set -o pipefail`** in strict scripts. Not the Unbound DNS resolver — that's [[DNS]] infrastructure software.

```bash
# default: echo $myvar  → empty line, exit 0
# set -u:  echo $myvar  → error, exit non-zero
```

## Standard config / commands

### Strict mode header (common pattern)

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

### Safe defaults

```bash
: "${HOME:?HOME must be set}"
PORT="${PORT:-8080}"           # default if unset
echo "${myvar:-fallback}"
```

### Check if set

```bash
if [[ -v myvar ]]; then
  echo "set to $myvar"
fi
```

### Temporarily disable (rare)

```bash
set +u
# legacy snippet that needs unset vars
set -u
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `unbound variable` on start | Line number in trace | `set -x`; assign var or use `${var:-}` |
| Works interactively, fails in CI | CI omits env | Export required env in workflow |
| `$1` empty in script | No args passed | `:${1:?usage: $0 file}` |
| Array unset | `set -u` + empty array | `"${arr[@]+"${arr[@]}"}"` pattern |
| Sourced script order | Parent `set -u` | Initialize before source |

## Gotchas

> [!WARNING]
> **`$?` immediately after** — test commands carefully with `set -e`.
>
> **`read var` without default** — can trip nounset on empty input in loops.
>
> **Don't confuse with Unbound DNS** — resolver config is `/etc/unbound/unbound.conf`.

## When NOT to use

- Don't enable `set -u` in ad-hoc interactive shells unless you enjoy surprise exits.
- Don't use empty default `:-` to hide missing required config — fail loud with `:?` for secrets/paths.

## Related

[[Linux/Bash/Bash functions]] [[Linux/Scripting]] [[Linux/commands/common commands]]
