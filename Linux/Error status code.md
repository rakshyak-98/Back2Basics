[[process]] [[bash flags]] [[systemd]] [[CLI]]

# Error status code

> Every Linux process exits with an 8-bit status (0–255) — shells, systemd, and CI pipelines use it to decide whether a step succeeded.

Convention: **0 = success**, **1–255 = failure** (meaning is program-specific except a few reserved values). Bash stores the last foreground exit code in `$?`. Pipelines use `$PIPESTATUS` unless `set -o pipefail` is enabled ([[bash flags]]).

## Common exit codes

| Code | Typical meaning |
|------|-----------------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of shell builtin / wrong arguments (`grep` no match is 1, not 2) |
| 126 | Command found but not executable |
| 127 | Command not found |
| 128+N | Killed by signal N (e.g. 137 = 128+9 SIGKILL) |
| 130 | Interrupted by SIGINT (Ctrl+C) |

## systemd service failures

```bash
systemctl status myapp.service
# Main PID: code=exited, status=1/FAILURE

journalctl -u myapp -n 50 --no-pager
```

| systemd hint | Meaning |
|--------------|---------|
| `status=203/EXEC` | `ExecStart` binary missing or not executable |
| `status=200/CHDIR` | `WorkingDirectory` invalid |
| `status=226/NAMESPACE` | Namespace setup failed |

## Scripts: test exit codes correctly

```bash
#!/bin/bash
set -euo pipefail

if grep -q error /var/log/app.log; then
  echo "errors present"
fi

# grep returns 1 when no match — don't use set -e blindly:
if ! grep -q pattern file; then
  echo "not found"
fi
```

## OOM and signal exits

Container or process killed by OOM often shows **137** (SIGKILL). See [[OOM (Linux Out Of Memory)]].

## Related

[[process]] · [[bash flags]] · [[systemd]] · [[bash script]]

## Sources

- `man 3 sysexits` (BSD conventions, not universal on Linux)
- `man 7 signal`
- [systemd.service(5) — ExecStart status](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
