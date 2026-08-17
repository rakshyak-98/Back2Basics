[[CLI]] [[grep]] [[Find command]] [[Scripting]] [[date]] [[ss]] [[journalctl]] [[lsof]]

# Common commands — daily ops cheat sheet

> Curated shell one-liners with interpretation — the 80% you reach for during incidents, deploys, and log hunts.

```txt
        Common commands —  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Not a memorization list

## Sources
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/) — overview
- [find(1)](https://man7.org/linux/man-pages/man1/find.1.html) — deep-dive

## Key Concepts
- **Navigate safely:** `pwd -P`, `realpath`, `cd -` for humans (not cron).
- **Size triage:** `du` finds hogs; `df` shows mount capacity.
- **Scoped search:** `grep -R` / `rg` with excludes beat searching `/`.
- **Preview before delete:** `find -print` before `-delete`.
- **Open files:** Deleted-but-open explains `df` vs `du` mismatches ([[lsof]]).


- **Core:** These commands answer recurring questions: where am I, what changed, what’s b…

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

## Mistakes to Avoid
- **Mistake:** `find . -delete` without `-type f` / depth limits
- **Mistake:** `grep -R` from `/` on production
- **Mistake:** Trusting `cd -` inside cron/systemd scripts

## Pros/Cons or Trade-offs
- **Pro:** Instant, scriptable, no extra tooling required.
- **Con:** Easy to cause damage with `rm`/`find -delete`; locale/`ps` parsing is fragile.
- **Trade-off:** One-liners for triage vs configuration management for lasting change.

## Comparison
- vs dedicated notes ([[grep]], [[Find command]], [[ss]]): this is a cheat shee…


### Use cases
- Disk-full incidents, finding stale logs, and scoping recursive greps during o…
