[[Linux/CLI]] [[Unbound]]

# unbound variable

> In Bash, an unbound variable is a name you reference before it is set — `set -u` (nounset) turns silent empty expansion into a hard error so scripts fail fast instead of corrupting data.

```txt
        unbound variable ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shell and SRE interviews use `set -u` to see whether you prevent empty-expans…

## Sources
- [GNU Bash Manual — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) — deep-dive

## Key Concepts
- **Default expansion:** unset names become empty string — dangerous in paths and arguments.
- **`set -u` (nounset):** referencing unset names aborts with “unbound variable.”
- **Strict mode trio:** `set -euo pipefail` fails fast on errors, unset names, and pipeline failures.
- **Safe defaults:** `${VAR:-default}`, `${VAR:?message}`, and `${VAR+x}` tests.


- **Core:** This note is about **shell variables**, not the [[Unbound]] DNS resolver. The…

## Technical Details
- Default Bash expands unset variables to empty string:

```bash
DIR=
rm -rf $DIR/*    # becomes rm -rf /* if DIR unset — catastrophic
```

- No error, no warning.

```bash
#!/usr/bin/env bash
set -u

echo "$MISSING"   # bash: MISSING: unbound variable
```

- Often combined in strict scripts:

```bash
set -euo pipefail
```

| Flag | Effect |
|------|--------|
| `-e` | Exit on first command failure |
| `-u` | Error on unbound variable |
| `-o pipefail` | Pipeline fails if any stage fails |

```bash
# Default value
echo "${DIR:-/tmp/safe}"

# Require variable
: "${API_KEY:?API_KEY must be set}"

# Check before use
if [[ -z "${DIR+x}" ]]; then
  echo "DIR not set" >&2
  exit 1
fi
```

## Mistakes to Avoid
- **Mistake:** Enabling `set -u` without fixing optional flags that were “empty…
- **Mistake:** Using `$DIR` unquoted even with nounset
- **Mistake:** Confusing this note with the [[Unbound]] recursive DNS server

## Pros/Cons or Trade-offs
- **Pro:** Converts silent empty expansion into immediate failure.
- **Con:** Breaks scripts that intentionally rely on unset → empty (must migrate to `${VAR-}` forms).
- **Con:** Alone, `set -u` does not quote expansions — still use `"$VAR"`.

## Comparison
- vs [[Unbound]] DNS: different topic entirely — resolver daemon vs Bash nounset.
- vs `set -e` alone: `-e` catches command failures


### Use cases
- Production deploy scripts, CI jobs, and operators’ one-liners that expand pat…

- **Example:** A cleanup cron with `rm -rf "$WORKDIR"/*` under `set -u` fails l…
