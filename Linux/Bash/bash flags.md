[[Bash]] [[bash script]] [[Bash syntax]]

# bash flags

> Bash flags (`set -o` / `bash -e`) change shell behavior — strict mode, debug traces, noclobber, and friends.

---

## Mental model

**Say it in one breath:** short flags (`-e`, `-u`, `-x`) are switches; `set -o name` is the long form; scripts should turn on the safe ones early.

```txt
bash -c '…'          one-shot string
set -euo pipefail    strict script defaults
set -x               print commands as run (debug)
set +x               turn trace off
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`-e` / `errexit`** | Exit on failure | “Don’t keep going after a failed deploy step.” |
| **`-u` / `nounset`** | Error on unset vars | “Catches typos in variable names.” |
| **`pipefail`** | Pipeline fails if any stage fails | “Without it, only the last command’s status counts.” |
| **`-x` / `xtrace`** | Trace execution | “Show what ran — great in CI logs.” |
| **`-n` / `noexec`** | Syntax check only | “`bash -n script.sh` before you ship.” |
| **`-C` / `noclobber`** | Don’t overwrite with `>` | “Force `>|` to clobber deliberately.” |

---

## Standard config / commands

**Script default:**

```bash
#!/usr/bin/env bash
set -euo pipefail
```

| Flag | Long (`set -o`) | Job |
|------|-----------------|-----|
| `-e` | `errexit` | Exit on non-zero |
| `-u` | `nounset` | Unset → error |
| `-x` | `xtrace` | Trace |
| `-n` | `noexec` | Parse only |
| `-v` | `verbose` | Print input lines |
| `-f` | `noglob` | Disable globs |
| `-C` | `noclobber` | Protect `>` overwrite |
| `-a` | `allexport` | Auto-export vars |
| `-b` | `notify` | Async job notifications |
| `-m` | `monitor` | Job control |
| `-i` | (invocation) | Force interactive |
| `-l` | (invocation) | Login shell |
| `-c` | (invocation) | Run string: `bash -c 'echo hi'` |
| `-r` | restricted | Restricted shell |
| `-P` | `physical` | `cd` follows physical paths |

```bash
set -e
set +e                 # disable
set -o pipefail
bash -n ./deploy.sh    # syntax check
bash -x ./deploy.sh    # run with trace
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Script exits “for no reason” | `-e` + command status | Log with `-x`; handle expected non-zero |
| Pipeline “succeeds” on failure | No `pipefail` | `set -o pipefail` |
| `unbound variable` | `-u` | Provide defaults `${x:-}` |
| Can’t overwrite file with `>` | `noclobber` | `>| file` or `set +C` |
| Trace too noisy | Blind `-x` | `set -x` around critical section only |

---

## Gotchas

> [!WARNING]
> **`set -e` is not a safety net for every construct** — commands in `if`, `&&`, `||`, and some pipelines are exempt; read Bash FAQ when surprised.

> [!WARNING]
> **`allexport` leaks env into every child** — easy to accidentally pass secrets.

> [!WARNING]
> **Restricted shell (`-r`) is not a security boundary** against determined users — use real isolation.

---

## When NOT to use

- **One-liner interactive exploration** — strict mode gets in the way; enable it in committed scripts.
- **Expecting `set -e` to replace real error handling** — still check critical commands explicitly.
- **Non-Bash `/bin/sh`** — `pipefail` and many `-o` names are Bash/ksh territory.

---

## Related

[[bash script]] [[Bash syntax]] [[Bash history]] [[Bash]]
