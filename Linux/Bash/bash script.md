[[Bash]] [[Bash syntax]] [[bash flags]] [[Bash functions]] [[Scripting]] [[bash sourcing other script]]

# bash script

> A bash script is a reproducible command file — shebang, arguments, tests, and loops so humans aren’t the runbook.

```txt
        bash script ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Expect a clean template: shebang, `set -euo pipefail`, `"$1"` quoting, exit c…

## Sources
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) — deep-dive
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) — overview

## Key Concepts
- **Shebang + chmod +x:** Make it directly runnable.
- **Strict mode:** See [[bash flags]].
- **Args:** `$1`, `$#`, `"$@"`.
- **`[[ ]]` tests / loops:** Control flow.
- **Functions:** Structure; see [[Bash functions]].


- **Core:** A script is a file executed by bash via shebang (`#!/usr/bin/env bash`) or `b…

## Technical Details
```bash
#!/usr/bin/env bash
set -euo pipefail

name="${1:-World}"
echo "Hello, ${name}"

echo "First: $1"
echo "All: $*"
echo "Count: $#"

read -r -p "Enter age: " age

if [[ "${age}" -gt 18 ]]; then
  echo "Adult"
elif [[ "${age}" -lt 18 ]]; then
  echo "Minor"
else
  echo "Exactly 18"
fi

for i in {1..5}; do
  echo "${i}"
done

count=1
while [[ "${count}" -le 5 ]]; do
  echo "${count}"
  ((count++)) || true
done

greet() {
  echo "Hello, ${1}!"
}
greet "World"

((sum = 5 + 3))
folder="beachside-hotel"
base="${folder%-hotel}"
```

```bash
chmod +x myscript.sh
./myscript.sh
bash -n myscript.sh
bash -x myscript.sh
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied | mode | `chmod +x` |
| Bad interpreter | CRLF / wrong shebang | `dos2unix`; fix path |
| Silent failure | no `set -e` | Add strict mode; check statuses |
| Word split bugs | unquoted `$1` | Quote always |

## Mistakes to Avoid
- **Mistake:** `#!/bin/sh` with bash-only syntax
- **Mistake:** Relying on interactive aliases/history
- **Mistake:** Ignoring exit codes in cron jobs

## Pros/Cons or Trade-offs
- **Pro:** Zero deps on Linux; perfect for glue.
- **Con:** Weak data structures; painful JSON/HTTP.
- **Trade-off:** Short Bash + [[jq]]/Python vs large Bash “apps.”

## Comparison
- vs interactive shell: scripts need strictness and absolute paths


### Use cases
- Deploy wrappers, backup hooks, and incident runbook automation with explicit …
