[[process]] [[bash flags]] [[systemd]] [[CLI]] [[bash script]] [[OOM (Linux Out Of Memory)]]

# Error status code

> Every Linux process exits with an 8-bit status (0–255) — shells, systemd, and CI pipelines use it to decide whether a step succeeded.

## Interview Relevance
Tests whether you read `$?`, interpret signal exits (137 = SIGKILL/OOM), and handle `grep`’s “no match = 1” under `set -e` without cargo-culting.

## Sources
- `man 7 signal` — deep-dive
- `man 3 sysexits` — overview (BSD conventions; not universal on Linux)
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive

## Core Definition
Convention: **0 = success**, **1–255 = failure** (meaning is program-specific except a few reserved patterns). Bash stores the last foreground exit code in `$?`. Pipelines need `$PIPESTATUS` or `set -o pipefail` — [[bash flags]].

## Key Concepts
- **Shell `$?`:** Last foreground command’s status.
- **Signal encoding:** `128 + signal_number` (e.g. 137 = 128+9 SIGKILL).
- **systemd status=:** Maps ExecStart failures to codes like `203/EXEC`.
- **pipefail:** Without it, a pipeline’s status is often only the last command.
- **Program-specific meanings:** Do not assume POSIX `sysexits` everywhere.

## Technical Details

| Code | Typical meaning |
|------|-----------------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of shell builtin / bad arguments (`grep` no match is 1, not 2) |
| 126 | Found but not executable |
| 127 | Command not found |
| 128+N | Killed by signal N (137 = SIGKILL) |
| 130 | SIGINT (Ctrl+C) |

```bash
systemctl status myapp.service
journalctl -u myapp -n 50 --no-pager
```

| systemd hint | Meaning |
|--------------|---------|
| `status=203/EXEC` | `ExecStart` missing or not executable |
| `status=200/CHDIR` | `WorkingDirectory` invalid |
| `status=226/NAMESPACE` | Namespace setup failed |

```bash
#!/bin/bash
set -euo pipefail

if ! grep -q pattern file; then
  echo "not found"
fi
```

OOM kills often surface as **137** — [[OOM (Linux Out Of Memory)]].

## Real-World Applications
CI fails a deploy stage when a health-check script exits non-zero; on-call maps systemd `status=203/EXEC` to a missing binary path after a bad package upgrade.

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable success/failure channel across languages and init systems.
- **Con:** Only 8 bits; rich error detail must go to logs/stderr. Conventions collide across tools.

## Comparison
vs HTTP status codes: process exit codes are local process lifecycle; HTTP codes are protocol responses. vs exceptions: exit codes survive process death for the parent/supervisor; in-process exceptions do not.

## Mistakes to Avoid
- Using `set -e` with bare `grep` when “no match” is a normal outcome (exit 1).
- Reading only the last pipeline status without `pipefail`.
- Treating 137 as “app bug” without checking OOM killer / cgroup memory events.
