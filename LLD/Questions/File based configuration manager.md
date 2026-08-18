[[Questions]] [[Design pattern/Singleton]]

# File based configuration manager

> Low-level design exercise — system-wide configuration manager with Singleton access and file-backed settings for a multi-module suite.

## Mental model

**Say it in one breath:** One configuration manager reads and writes shared config files so every module sees consistent settings without each opening files independently.

### Problem statement

Create a **system-wide configuration manager** for a complex software suite. The manager should:

- Maintain a **single source of truth** for configuration values.
- Read from and write to **file-based** storage.
- Expose thread-safe access through a **Singleton** instance.

### Typical operations

| Operation | Purpose |
| --- | --- |
| `load(path)` | Parse configuration file into memory |
| `get(key)` | Read a setting |
| `set(key, value)` | Update a setting (may persist to disk) |
| `save()` | Flush in-memory changes to file |
| `reload()` | Re-read from disk after external edits |

## Standard config / commands

```python
config = ConfigManager.get_instance()
config.load("/etc/myapp/config.yaml")
timeout = config.get("db.timeout")
config.set("db.timeout", 30)
config.save()
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Stale config in running process | File changed on disk | Call `reload()` or watch file with inotify |
| Race on concurrent writes | Missing lock | Synchronize `set` / `save` |
| Partial write corrupts file | Crash mid-save | Atomic write (temp file + rename) |

## Gotchas

> [!WARNING]
> **Global mutable config** — document which keys are hot-reloadable versus restart-required.

## When NOT to use

- **Twelve-factor apps** — environment variables and secret managers often replace file-based global config.

## Related

[[Design pattern/Singleton]] [[Questions]] [[LLD/Questions/Logger]]
