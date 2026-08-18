[[Questions]] [[Design pattern/Singleton]] [[LLD/Questions/Connection Pool]]

# Logger

> Low-level design exercise — implement a thread-safe Singleton logger that writes timestamped levels to one shared log file.

## Mental model

**Say it in one breath:** One logger instance, one log file, synchronized writes — Singleton prevents duplicate file handles and conflicting writes.

### Problem statement

Develop a logging module that maintains a **single log file** for the application. Use the **Singleton** pattern so only one logger exists and access is thread-safe.

### Requirements

**Part 1 — Singleton**

- `LoggerImpl` implements `Logger`.
- `get_instance()` returns the singleton.
- `reset_instance()` clears it (for tests).

**Part 2 — Logging**

| Method | Behavior |
| --- | --- |
| `set_log_file(path)` | Set output file (use `TextIO`) |
| `log(level, message)` | Timestamp + level + message; error if file not set |
| `get_log_file()` | Return current path |
| `flush()` | Flush buffered entries |
| `close()` | Release resources |

## Standard config / commands

```python
logger = LoggerImpl.get_instance()
logger.set_log_file("/var/log/app.log")
logger.log("INFO", "service started")
logger.flush()
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Log file empty | `flush()` not called | Call `flush()` after writes or on shutdown |
| Duplicate loggers | Multiple `get_instance` races | Lock around lazy initialization |
| Tests interfere | Static instance persists | Call `reset_instance()` in `tearDown` |

## Gotchas

> [!WARNING]
> **Logging before `set_log_file`** — must throw; callers must initialize first.

## When NOT to use

- **Structured logging at scale** — use append-only streams, rotation, and centralized collectors instead of a hand-rolled singleton file.

## Related

[[Design pattern/Singleton]] [[Questions]] [[LLD/Questions/Connection Pool]]
