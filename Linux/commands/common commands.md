[[CLI]] [[grep]] [[Find command]] [[Scripting]]

# Common commands — daily ops cheat sheet

> One-line: **curated shell one-liners with interpretation** — the 80% you reach for during incidents, deploys, and log hunts. Not exhaustive; each line says *what it proves*.

## Mental model

These commands answer recurring questions: *where am I*, *what changed*, *what's big*, *who owns this port*, *what's in these files*. Prefer flags that reduce noise (`-type f`, `--exclude-dir`) before piping to `grep`.

## Standard config / commands

### Navigation & paths

```bash
cd -                    # Jump to $OLDPWD — previous directory after cd elsewhere
pwd -P                  # Physical path (resolves symlinks); use in scripts
realpath ./relative     # Absolute path without cd
mkdir -p a/b/c          # Create tree; no error if exists (-p)
```

### Find & size

```bash
find . -type f -size +100M -printf '%s %p\n' | sort -rn | head
# +100M = larger than 100 MiB blocks; add -mtime +30 for stale large files

find /var/log -type f -name '*.log' -mtime +14 -ls
# Logs older than 14 days — candidate for rotation/archive

du -sh */ | sort -hr | head
# Which top-level dirs dominate disk — first pass before find
```

### Search in trees

```bash
grep -R --exclude-dir={.git,node_modules,dist} 'pattern' .
# Recursive; skip VCS and build artifacts

grep -RIn 'ERROR' /var/log/app/ --include='*.log'
# -I skip binary, -n line numbers — incident triage

rg 'pattern' --glob '!node_modules'    # ripgrep: faster default on large trees
```

### Process & disk quick checks

```bash
ps aux --sort=-%mem | head -20         # Who ate RAM
df -hT                                 # Mount + fstype; spot 100% partitions
lsof +D /path/to/dir 2>/dev/null       # What's open under dir (umount failures)
```

### Safe destructive preview

```bash
find . -name '*.tmp' -print           # ALWAYS print before -delete
find . -name '*.tmp' -delete          # Only after print looks right

rm -rf ./build/*                      # Trailing /* avoids rm -rf mistake on wrong dir
```

### Archives & permissions

```bash
tar czf backup-$(date +%F).tar.gz --exclude=node_modules project/
chmod -R u+rwX,go-rwx sensitive_dir/  # Capital X = dirs only get +x
```

### Time & identity

```bash
date -u +%Y-%m-%dT%H:%M:%SZ           # ISO UTC for logs/tickets
id; groups; whoami                    # Effective user + supplementary groups
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "No space left on device" | `df -h`; `du -sh /*` | `find` large files; rotate logs; expand volume |
| Can't delete file | `lsof +D .` | Stop process holding FD; not a chmod issue |
| grep too slow / wrong hits | `--include`, `--exclude-dir` | Narrow path; use `rg` |
| Script cd'd wrong place | `pwd -P`; `realpath` | Use absolute paths in cron/systemd |
| find deleted too much | `-print` first | Restore from backup; add `-maxdepth` guard |

## Gotchas

> [!WARNING]
> **`find . -delete` without `-type f`** — can remove directories unexpectedly. Always constrain type and depth.

> [!WARNING]
> **`grep -R` on /** — IO storm. Scope to `/var/log`, app dir, or use `-m 1` to cap matches.

- **`cd -` in scripts** — `$OLDPWD` is shell state; don't rely on it in non-interactive cron without explicit cd.
- **`du` vs `df` mismatch** — deleted but open files (`lsof \| grep deleted`); restart process or reboot.

## When NOT to use

- **Production config changes** — use config management + review, not ad-hoc one-liners from this sheet.
- **Security audit** — need dedicated tools ([[nmap]], [[ss]], policy scanners), not find/grep alone.

## Related

[[CLI]] [[grep]] [[Find command]] [[Scripting]] [[date]] [[ss]] [[journalctl]]
