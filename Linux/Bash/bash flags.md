[[Bash]] [[bash script]] [[Bash syntax]] [[Scripting]]

# bash flags

> Bash flags (`set -o` / `bash -e`) change shell behavior — strict mode, debug traces, noclobber, and friends.

```txt
        bash flags ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** `set -euo pipefail` is the expected baseline

## Sources
- [Bash Reference — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) — deep-dive
- [BashFAQ — set -e](https://mywiki.wooledge.org/BashFAQ/105) — deep-dive

## Key Concepts
- **`-e` (errexit):** Exit when a command fails (with caveats in `if`/`&&` lists).
- **`-u` (nounset):** Error on unset variable expansion.
- **`-o pipefail:** Pipeline fails if any stage fails, not only the last.
- **`-x` (xtrace):** Print commands — debug gold.
- **`bash -n`:** Syntax check without running.


- **Core:** `set -o option` (or short `-e`, `-u`, …) toggles shell options for the curren…

## Technical Details
```bash
#!/usr/bin/env bash
set -euo pipefail

set -e
set +e                 # disable
set -o pipefail
bash -n ./deploy.sh
bash -x ./deploy.sh
set -x
# …
set +x

set -o noclobber       # refuse > overwrite
set -o nounset
```

| Flag / option | Effect |
|---------------|--------|
| `-e` | Exit on error |
| `-u` | Unset var = error |
| `pipefail` | Any pipe stage failure counts |
| `-x` | Trace |
| `noclobber` | Block `>` overwrite |
| `noglob` | Disable pathname expansion |

| Symptom | Check | Fix |
|---------|-------|-----|
| Script continues after fail | no `-e` / exception context | Add `-e`; don’t hide in `cmd \|\| true` casually |
| Pipeline “succeeds” on mid fail | default pipe status | `set -o pipefail` |
| Trace too noisy | whole script `-x` | Wrap critical section only |
| `nounset` on optional arg | `${1}` | Use `${1:-}` |

## Mistakes to Avoid
- **Mistake:** Believing `-e` covers every failure mode (read the FAQ exception…
- **Mistake:** Leaving `set -x` on in production cron (secret leakage in logs)
- **Mistake:** Using `cmd || true` everywhere “to satisfy -e.”

## Pros/Cons or Trade-offs
- **Pro:** Catches silent failures early.
- **Con:** `-e` semantics surprise people in conditionals; over-tracing hides signal.
- **Trade-off:** Strict scripts vs temporary `set +e` around expected failures.

## Comparison
- vs language exceptions: shell uses exit statuses + options


### Use cases
- Making CI deploy scripts fail loudly, tracing a flaky install with `bash -x`,…
