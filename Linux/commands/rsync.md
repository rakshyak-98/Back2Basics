[[diff]] [[SSH]] [[Linux file management]] [[file mount]]

# rsync

> One-line: **delta file sync over SSH or local** — production backups and deploys with `-a`, dry-run, and explicit trailing slashes. The trailing slash rule causes more outages than rsync bugs.

## Mental model

rsync compares file lists and transfers **changed blocks** (rolling checksum). Archive mode `-a` preserves permissions, times, symlinks, recursion — your default for backups. **Source/dest slash semantics** determine whether you copy *contents* or the *directory itself*.

```
src/  dest/   → contents of src INTO dest (merge)
src   dest/   → creates dest/src/ (whole dir)
--delete      → dest files not in src are REMOVED (mirror)
```

| Flag | Meaning |
|------|---------|
| `-a` | Archive (rlptgoD) — preserve metadata |
| `-v` | Verbose |
| `-z` | Compress over network |
| `-n` | Dry run — **always first on prod** |
| `-c` | Checksum compare (ignore mtime) |
| `-H` | Hard links (backup fidelity) |
| `--delete` | Delete extraneous dest files |
| `-e ssh` | Remote shell (custom key/port) |

## Standard config / commands

**Safe backup pattern:**

```bash
# Dry run first — read output
rsync -avhn --delete /data/app/ /backup/app-$(date +%F)/
# Happy? remove n
rsync -avh --delete /data/app/ /backup/app-$(date +%F)/
```

**Remote over SSH:**

```bash
rsync -avz -e "ssh -i ~/.ssh/deploy -p 2222" \
  ./dist/ user@host:/var/www/app/

# Restricted key in authorized_keys:
# command="rsync --server -logDtpre.iLsfxC . /path",no-port-forwarding ...
```

**Exclude noise:**

```bash
rsync -av --exclude='node_modules' --exclude='.git' \
  project/ user@host:/opt/project/
```

**Verify before cutover ([[diff]] complement):**

```bash
rsync -avnc --delete staging/ prod/   # checksum dry-run — lists would-change
```

**Bandwidth limit (shared link):**

```bash
rsync -av --bwlimit=5000 src/ dest/   # KB/s
```

**Partial transfers resume:**

```bash
rsync -avP src/ dest/   # -P = --partial --progress
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty dest after sync | Trailing slash mistake | `src/` vs `src`; re-run with correct path |
| Deleted prod files | `--delete` wrong direction | Restore from backup; **dest is receiver** — read command twice |
| Permission denied | UID mismatch; `-a` as non-root | `--rsync-path="sudo rsync"` or align ownership |
| All files re-copied | Clock skew; different ownership | `-c` for content; fix NTP; `--no-owner` if intentional |
| SSH hangs | Firewall; wrong key | `ssh -v`; `-e "ssh -o BatchMode=yes"` |
| Disk full mid-sync | `--delete` + partial | `-P`; monitor dest; btrfs snapshot first |
| Special files skipped | xattrs/ACLs | `-X` xattrs, `-A` ACLs (needs support both sides) |

## Gotchas

> [!WARNING]
> **`rsync -av --delete src/ dest/` with reversed paths** — mirrors wrong way and wipes production. Tattoo: *receiver is last argument*.

> [!WARNING]
> **NFS + `-a`** — permission mapping lies across UID domains. Use `--numeric-ids` or consistent UID/GID maps.

- **Running rsync while app writes** — inconsistent backup; quiesce DB ([[WAL (Write-Ahead Log)]] snapshot) or use filesystem snapshot + rsync snapshot mount.
- **Cron without `-n` review** — typo in path deletes at 3am.
- **`-z` on LAN** — CPU cost; often slower on 10G local.

## When NOT to use

- **Live database files** — raw copy of PostgreSQL/MySQL datadir without snapshot = corruption risk.
- **Bidirectional sync with conflicts** — use Syncthing, git, or dedicated tools; rsync last-writer-wins.
- **Many small files over high latency** — tar+ssh stream sometimes wins (`tar czf - . | ssh host tar xzf - -C dest`).

## Related

[[diff]] [[SSH]] [[Linux file management]] [[file mount]]
