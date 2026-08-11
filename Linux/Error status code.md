[[Linux]] [[process]] [[Linux/commands/gdb]] [[OOM (Linux Out Of Memory)]]

# Error status code

> Exit status is the 8-bit code a process returns to its parent — `0` means success; non-zero means failure or death by signal.

---

## Mental model

**Say it in one breath:** Shell and supervisors only see a small integer; conventions map common failures, and `128+N` means “killed by signal N.”

```txt
program ends
   │
   ├─ exit(0) / return 0     → success
   ├─ exit(1..125)           → app/shell-defined error
   └─ killed by signal N     → status 128+N  (e.g. SIGKILL → 137)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Exit status** | Byte parent waits on | “`waitpid` fills it; shell exposes `$?`.” |
| **0** | Success | “Unix convention: zero is OK.” |
| **Non-zero** | Failure (broad) | “Any non-zero fails `set -e` pipelines carefully.” |
| **126 / 127** | Not executable / not found | “Permission vs PATH — different fixes.” |
| **128 + N** | Killed by signal N | “137 → SIGKILL; 139 → SIGSEGV.” |
| **errno** | Per-syscall error | “Not the same as process exit code.” |

### Common codes (say these)

| Code | Meaning |
|------|---------|
| **0** | Success |
| **1** | General error |
| **2** | Misuse of shell builtin (common convention) |
| **126** | Found but not executable (permission / not a binary) |
| **127** | Command not found |
| **130** | Terminated by SIGINT (Ctrl-C) — `128+2` |
| **137** | SIGKILL — `128+9` (OOM killer often) |
| **139** | SIGSEGV — `128+11` |
| **143** | SIGTERM — `128+15` |
| **255** | Out of range / wrapped / `exit(-1)` |

---

## Standard config / commands

```bash
true; echo $?          # 0
false; echo $?         # 1
./missing; echo $?     # 127
bash -c 'kill -9 $$'; echo $?   # 137 in parent

# Scripts
set -euo pipefail
cmd || { echo "failed: $?"; exit 1; }

# From C
exit(code);            # only low 8 bits matter
```

```c
#include <sys/wait.h>
int status;
waitpid(pid, &status, 0);
if (WIFEXITED(status))   code = WEXITSTATUS(status);
if (WIFSIGNALED(status)) sig  = WTERMSIG(status);
```

| Knob | Why it matters |
|------|----------------|
| `set -e` | Abort on non-zero — know pipefail interactions |
| `pipefail` | Pipeline status = rightmost non-zero (bash) |
| systemd `SuccessExitStatus=` | Treat some non-zero as OK for the unit |
| Container `restartPolicy` | Restarts keyed off exit code |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Exit 127 | `which cmd`; PATH in service env | Install binary; fix unit `Environment=` |
| Exit 126 | `ls -l`; noexec mount | `chmod +x`; fix mount options |
| Exit 137 | `dmesg` OOM; `kill -9` | Memory limit / leak — [[OOM (Linux Out Of Memory)]] |
| Exit 139 | core / gdb `bt` | Fix segfault — [[Stack trace]] |
| Exit 1, vague | App logs; run foreground | Don’t guess — print your own codes |

---

## Gotchas

> [!WARNING]
> **Only 8 bits.** `exit(256)` becomes `0` — success by accident.

> [!WARNING]
> **`$?` after a pipeline** without `pipefail` is the last command — earlier failures hide.

> [!WARNING]
> **137 is not “app error 137”.** Decode as signal before reading app docs.

> [!WARNING]
> **errno ≠ exit code.** A failed `read` sets errno; the process may still `exit(0)` if you ignore it.

---

## When NOT to use

- **Rich error detail** — use stderr messages / structured logs; status is a coarse summary.
- **Cross-machine RPC** — map to HTTP/gRPC codes explicitly; don’t leak raw Unix statuses.
- **Distinguishing 50 app failures** — stick to small reserved sets; document them.

---

## Related

[[process]] [[Linux Process Theory]] [[OOM (Linux Out Of Memory)]] [[Stack trace]] [[gdb]] [[systemctl]] [[journalctl]]
