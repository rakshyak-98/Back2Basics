[[DNS]] · [[Unbound]] · [[Linux/CLI]]

# unbound variable

> In Bash, an unbound variable is a name you reference before it is set — `set -u` (nounset) turns silent empty expansion into a hard error so scripts fail fast instead of corrupting data.

---

## The problem

Default Bash expands unset variables to empty string:

```bash
DIR=
rm -rf $DIR/*    # becomes rm -rf /* if DIR unset — catastrophic
```

No error, no warning.

## nounset (`set -u`)

```bash
#!/usr/bin/env bash
set -u

echo "$MISSING"   # bash: MISSING: unbound variable
```

Often combined in strict scripts:

```bash
set -euo pipefail
```

| Flag | Effect |
|------|--------|
| `-e` | Exit on first command failure |
| `-u` | Error on unbound variable |
| `-o pipefail` | Pipeline fails if any stage fails |

## Safe patterns

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

## Not DNS Unbound

This note is about **shell variables**, not the [[Unbound]] DNS resolver. Filename kept for vault search history.

## Recall

- What does `set -u` change about `$UNDEFINED` in a script?
- Why pair `set -u` with `set -e` in production shell scripts?

## Sources

- [GNU Bash Manual — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
- [RFC 1123 — robustness](https://datatracker.ietf.org/doc/html/rfc1122) (general fail-fast spirit)
