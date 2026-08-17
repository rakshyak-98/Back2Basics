[[Commands]] [[FileManagement]] [[rsync]] [[grep]] [[zip]]

# Find command

> find walks a directory tree and selects files by name, time, size, or owner — then prints or runs a command on them.

```txt
        Find command ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Ops safety: predicates before `-delete`, `-mtime` sign meaning, `-exec … {} +…

## Sources
- [find(1)](https://man7.org/linux/man-pages/man1/find.1.html) — deep-dive
- [GNU Findutils manual](https://www.gnu.org/software/findutils/manual/html_node/find_html/index.html) — overview

## Key Concepts
- **Predicates:** `-name`, `-type`, `-mtime`, `-size`, `-user`, `-perm`.
- **Actions:** `-print`, `-delete`, `-exec cmd {} +` (batched).
- **`-mtime +N`:** Modified more than N*24h ago (sign matters).
- **`-delete`:** Implies depth-first — still preview first.
- **Safety:** Scope path; constrain `-type f`; avoid `/` roots.


- **Core:** `find` descends from a path, applies boolean predicates, then an action (`-pr…

## Technical Details
```bash
find . -name '*.txt'
find /var/log -type f -name '*.log'
find /path -type d -empty
find /path -type f -empty

find /home -mtime -30
find . -mtime -7
find . -size +10M
find /srv -user root
find . -perm 644

find . -name '*.log' -print          # preview
find . -name '*.log' -delete
find . -type f -exec chmod 644 {} +
find . -name '*.log' -exec rm -f {} +

find /path -maxdepth 2 -mindepth 1 -type d
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Deleted too much | No `-type`/`-maxdepth` | Restore backup; tighten predicates |
| Wrong age matches | `+`/`-` confusion | Re-read `-mtime`/`-mmin` signs |
| Slow on huge trees | Unscoped find | Add depth; use `fd`/`locate` when appropriate |
| Permission errors | Unreadable dirs | `sudo` or narrow path; `-readable` |

## Mistakes to Avoid
- **Mistake:** `-delete` without a prior `-print` dry run
- **Mistake:** Misreading `-mtime +0` as “today.”
- **Mistake:** Unscoped `find / … -exec rm`

## Pros/Cons or Trade-offs
- **Pro:** Precise, portable, scriptable tree queries.
- **Con:** Destructive actions are unforgiving; easy to over-match.
- **Trade-off:** `find` for criteria vs `du`/`ncdu` for “what’s big” UX.

## Comparison
- vs [[grep]] `-r`: content search vs metadata selection


### Use cases
- Purging logs older than 14 days, finding large files on a full disk, and batc…
