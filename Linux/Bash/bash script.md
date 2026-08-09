[[Bash]] [[Bash syntax]] [[bash flags]]

# bash script

> A bash script is a reproducible command file — shebang, arguments, tests, and loops so humans aren’t the runbook.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** start with `#!/usr/bin/env bash`, fail fast with `set -euo pipefail`, quote everything, treat `$1`/`$@` as inputs.

```txt
shebang → set flags → parse args → do work → exit status
chmod +x  &&  ./script.sh args…
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Shebang** | Interpreter line | “Kernel uses it when you `./script`.” |
| **`set -euo pipefail`** | Strict mode | “Exit on error, unset var, and failed pipe stage.” |
| **`$1` / `$@` / `$#`** | Args | “Positional params are the CLI.” |
| **`[[ -f ]]`** | File tests | “Existence checks before you `rm`.” |
| **Functions** | Named blocks | “Reuse; still quote `"$1"` inside.” |

---

## Standard config / commands

```bash
#!/usr/bin/env bash
set -euo pipefail

name="${1:-World}"
echo "Hello, ${name}"

# Args
echo "First: $1"
echo "All: $*"
echo "Count: $#"

# Input
read -r -p "Enter age: " age

# Tests
if [[ "${age}" -gt 18 ]]; then
  echo "Adult"
elif [[ "${age}" -lt 18 ]]; then
  echo "Minor"
else
  echo "Exactly 18"
fi

# Loops
for i in {1..5}; do
  echo "${i}"
done

count=1
while [[ "${count}" -le 5 ]]; do
  echo "${count}"
  ((count++)) || true
done

# Functions
greet() {
  echo "Hello, ${1}!"
}
greet "World"

# Arithmetic / strings
((sum = 5 + 3))
folder="beachside-hotel"
base="${folder%-hotel}"          # strip suffix
```

Make runnable:

```bash
chmod +x myscript.sh
./myscript.sh
```

File tests: `-f` file, `-d` dir, `-e` exists. Number ops: `-eq -ne -lt -gt -le -ge`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `./script: Permission denied` | Mode | `chmod +x` |
| Runs under `sh` differently | Shebang / `sh script` | Invoke `./script` or `bash script` |
| Dies on `((count++))` with `-e` | Exit status 1 when was 0 | `((count++)) \|\| true` or `count=$((count+1))` |
| “unbound variable” | `set -u` | Default: `${1:-}` |
| Broken if/fi | Typo `if`/`fi` | Match `then`/`fi`; use `[[` |

---

## Gotchas

> [!WARNING]
> **Unquoted expansions** are the #1 script CVE class — `"$var"` always.

> [!WARNING]
> **`set -e` is subtle with pipes and `if`** — prefer `set -euo pipefail` *and* understand exceptions; test failure paths.

> [!WARNING]
> **Windows CRLF shebangs** — `bad interpreter: /bin/bash^M` → `dos2unix`.

---

## When NOT to use

- **Complex data / HTTP / JSON APIs as core logic** — Python/Go; bash as wrapper.
- **Performance-critical loops over huge files** — awk/compiled tools.
- **Secrets in the script body** — inject via env/files with mode 600.

---

## Related

[[Bash syntax]] [[bash flags]] [[Bash history]] [[jq]] [[awk]] [[Bash]]
