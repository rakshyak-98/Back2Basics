[[commands]] [[FileManagement]] [[rsync]]

# Find command

> `find` walks a directory tree and selects files by name, time, size, owner — then prints or runs a command on them.

## Mental model

**Say it in one breath:** start at a path, apply tests (`-name`, `-mtime`, …), then an action (`-print`, `-delete`, `-exec`).

```txt
path ──► descend ──► match predicates ──► action
              -maxdepth limits how deep
              {} + batches like xargs
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`-type f/d/l`** | File / dir / symlink | “Narrow before you delete.” |
| --- | --- | --- |
| **`-name` / `-iname`** | Glob match | “Quoted globs — shell must not expand them.” |
| **`-mtime -7`** | Modified in last 7 days | “Negative means *within*; positive means *older than*.” |
| **`-exec … {} +`** | Run command in batches | “`+` is fast; `\;` forks once per file.” |
| **`-delete`** | Remove matches | “Depth-first; safer than naive `rm` loops.” |

## Standard config / commands

```bash
# Names / types
find . -name '*.txt'
find /var/log -type f -name '*.log'
find /path -type d -empty
find /path -type f -empty

# Time / size / owner
find /home -mtime -30
find . -mtime -7
find . -size +10M
find /srv -user root
find . -perm 644

# Actions
find . -name '*.log' -delete
find . -type f -exec chmod 644 {} +
find . -name '*.log' -exec rm -f {} +

# Depth
find /path -maxdepth 2 -mindepth 1 -type d
```

| Part | Meaning |
| --- | --- |
| `{}` | Placeholder for matched path |
| `+` | Batch many paths into one command |
| `\;` | One invocation per file (slow) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Shell expands `*.log` early | Unquoted pattern | Quote: `-name '*.log'` |
| Deleted too much | No dry-run | `find … -print` first; then `-delete` |
| Permission errors | Unreadable dirs | Run with needed privs; or `-ignore_readdir_race` |
| Slow on huge trees | Full walk | `-maxdepth`; locate/mlocate for name-only |
| `-type -f` typo | Extra dash | `-type f` |

## Gotchas

> [!WARNING]
> **`-mtime +0` means older than 24h**, not “today”. Read the man page signs carefully.

> [!WARNING]
> **`-delete` implies `-depth`** — good for dirs; still test with `-print`.

> [!WARNING]
> **Never `find / -exec rm`** without extreme filters — one bad predicate is disaster.

## When NOT to use

- **Interactive fuzzy file pick** — `fzf`, IDE search.
- **Content search** — [[grep]] / `rg` (find locates *names*, not text).
- **Sync trees** — [[rsync]].

## Related

[[grep]] [[rsync]] [[zip]] [[commands]]
