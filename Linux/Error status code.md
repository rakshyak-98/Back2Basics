[[process]] [[bash flags]] [[systemd]] [[NodeJS CLI]] [[bash script]] [[OOM (Linux Out Of Memory)]]

# Error status code

> Every Linux process exits with an 8-bit status (0–255) — shells, systemd, and CI pipelines use it to decide whether a step succeeded.

```txt
        Error status code ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Tests whether you read `$?`, interpret signal exits (137 = SIGKILL/OOM), and …

## Sources
- `man 7 signal` — deep-dive
- `man 3 sysexits` — overview (BSD conventions; not universal on Linux)
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive

## Key Concepts
- **Shell `$?`:** Last foreground command’s status.
- **Signal encoding:** `128 + signal_number` (e.g. 137 = 128+9 SIGKILL).
- **systemd status=:** Maps ExecStart failures to codes like `203/EXEC`.
- **pipefail:** Without it, a pipeline’s status is often only the last command.
- **Program-specific meanings:** Do not assume POSIX `sysexits` everywhere.


- **Core:** Convention: **0 = success**, **1–255 = failure** (meaning is program-specific…

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

- OOM kills often surface as **137** — [[OOM (Linux Out Of Memory)]].

## Mistakes to Avoid
- **Mistake:** Using `set -e` with bare `grep` when “no match” is a normal outc…
- **Mistake:** Reading only the last pipeline status without `pipefail`
- **Mistake:** Treating 137 as “app bug” without checking OOM killer / cgroup m…

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable success/failure channel across languages and init systems.
- **Con:** Only 8 bits; rich error detail must go to logs/stderr. Conventions collide across tools.

## Comparison
- vs HTTP status codes: process exit codes are local process lifecycle


### Use cases
- CI fails a deploy stage when a health-check script exits non-zero
