[[Bash]] [[bash script]] [[Bash syntax]] [[Scripting]]

# bash flags

> Bash flags (`set -o` / `bash -e`) change shell behavior — strict mode, debug traces, noclobber, and friends.





## Interview Relevance
`set -euo pipefail` is the expected baseline; know what each letter does and that `-e` has subtle exceptions.

## Sources
- [Bash Reference — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) — deep-dive
- [BashFAQ — set -e](https://mywiki.wooledge.org/BashFAQ/105) — deep-dive

## Core Definition
`set -o option` (or short `-e`, `-u`, …) toggles shell options for the current shell. Scripts typically start with `set -euo pipefail`. `bash -x` / `set -x` traces commands as they run.

## Key Concepts
- **`-e` (errexit):** Exit when a command fails (with caveats in `if`/`&&` lists).
- **`-u` (nounset):** Error on unset variable expansion.
- **`-o pipefail:** Pipeline fails if any stage fails, not only the last.
- **`-x` (xtrace):** Print commands — debug gold.
- **`bash -n`:** Syntax check without running.

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

## Real-World Applications
Making CI deploy scripts fail loudly, tracing a flaky install with `bash -x`, and preventing accidental overwrite with `noclobber`.

## Pros/Cons or Trade-offs
- **Pro:** Catches silent failures early.
- **Con:** `-e` semantics surprise people in conditionals; over-tracing hides signal.
- **Trade-off:** Strict scripts vs temporary `set +e` around expected failures.

## Comparison
vs language exceptions: shell uses exit statuses + options. vs `shellcheck`: static analysis complements runtime flags. Related: [[bash script]].

## Mistakes to Avoid
- Believing `-e` covers every failure mode (read the FAQ exceptions).
- Leaving `set -x` on in production cron (secret leakage in logs).
- Using `cmd || true` everywhere “to satisfy -e.”
