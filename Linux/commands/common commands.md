[[CLI]] [[grep]] [[Find command]] [[Scripting]] [[date]] [[ss]] [[journalctl]] [[lsof]]

# Common commands — daily ops cheat sheet

> Curated shell one-liners with interpretation — the 80% you reach for during incidents, deploys, and log hunts.

## Interview Relevance
Not a memorization list — shows you pick the right tool for “what’s big,” “who holds this,” and “safe delete preview,” with flags that reduce noise.

## Sources
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/) — overview
- [find(1)](https://man7.org/linux/man-pages/man1/find.1.html) — deep-dive

## Core Definition
These commands answer recurring questions: where am I, what changed, what’s big, who owns this port, what’s in these files. Prefer flags that reduce noise (`-type f`, `--exclude-dir`) before piping to grep.

## Key Concepts
- **Navigate safely:** `pwd -P`, `realpath`, `cd -` for humans (not cron).
- **Size triage:** `du` finds hogs; `df` shows mount capacity.
- **Scoped search:** `grep -R` / `rg` with excludes beat searching `/`.
- **Preview before delete:** `find -print` before `-delete`.
- **Open files:** Deleted-but-open explains `df` vs `du` mismatches ([[lsof]]).

## Technical Details

```bash
cd -
pwd -P
realpath ./relative
mkdir -p a/b/c

find . -type f -size +100M -printf '%s %p\n' | sort -rn | head
find /var/log -type f -name '*.log' -mtime +14 -ls
du -sh */ | sort -hr | head

grep -R --exclude-dir={.git,node_modules,dist} 'pattern' .
grep -RIn 'ERROR' /var/log/app/ --include='*.log'
rg 'pattern' --glob '!node_modules'

ps aux --sort=-%mem | head -20
df -hT
lsof +D /path/to/dir 2>/dev/null

find . -name '*.tmp' -print
find . -name '*.tmp' -delete

tar czf backup-$(date +%F).tar.gz --exclude=node_modules project/
chmod -R u+rwX,go-rwx sensitive_dir/

date -u +%Y-%m-%dT%H:%M:%SZ
id; groups; whoami
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No space left | `df -h`; `du -sh /*` | Large files; rotate logs; expand volume |
| Can't delete file | `lsof +D .` | Stop process holding FD |
| grep too slow | `--include`, `--exclude-dir` | Narrow path; use `rg` |
| find deleted too much | `-print` first | Backup; add `-maxdepth` / `-type f` |

## Real-World Applications
Disk-full incidents, finding stale logs, and scoping recursive greps during outages without thrashing the whole filesystem.

## Pros/Cons or Trade-offs
- **Pro:** Instant, scriptable, no extra tooling required.
- **Con:** Easy to cause damage with `rm`/`find -delete`; locale/`ps` parsing is fragile.
- **Trade-off:** One-liners for triage vs configuration management for lasting change.

## Comparison
vs dedicated notes ([[grep]], [[Find command]], [[ss]]): this is a cheat sheet hub; those notes go deep. vs security scanners: find/grep are not an audit program.

## Mistakes to Avoid
- `find . -delete` without `-type f` / depth limits.
- `grep -R` from `/` on production.
- Trusting `cd -` inside cron/systemd scripts.
