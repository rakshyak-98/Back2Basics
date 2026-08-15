[[diff]] [[SSH]] [[Linux file management]] [[file mount]]

# rsync

> Delta file sync over SSH or local — backups and deploys with `-a`, dry-run, and careful trailing slashes.

## Interview Relevance

Classic operations question: trailing-slash semantics, `--delete` danger, and always dry-run (`-n`) before production mirrors.

## Sources

- [rsync man page](https://download.samba.org/pub/rsync/rsync.1) — deep-dive
- [Wikipedia — rsync](https://en.wikipedia.org/wiki/Rsync) — overview

## Core Definition

rsync compares file lists and transfers changed blocks (rolling checksum). Archive mode `-a` preserves permissions, times, symlinks, and recursion — the usual default for backups.

## Key Concepts

- **Trailing slash:** `src/` copies contents into dest; `src` creates `dest/src/`.
- **`--delete`:** removes extras on the receiver — wrong direction wipes production.
- **`-n` dry run:** always first on production paths.
- **`-a` archive:** `rlptgoD` metadata preservation.
- **Receiver is last:** tattoo this before any `--delete` command.

## Technical Details

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
| `-n` | Dry run |
| `-c` | Checksum compare (ignore mtime) |
| `-H` | Hard links |
| `--delete` | Delete extraneous dest files |
| `-e ssh` | Remote shell |

```bash
rsync -avhn --delete /data/app/ /backup/app-$(date +%F)/
rsync -avh --delete /data/app/ /backup/app-$(date +%F)/

rsync -avz -e "ssh -i ~/.ssh/deploy -p 2222" \
  ./dist/ user@host:/var/www/app/

rsync -av --exclude='node_modules' --exclude='.git' \
  project/ user@host:/opt/project/

rsync -avnc --delete staging/ prod/
rsync -av --bwlimit=5000 src/ dest/
rsync -avP src/ dest/
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty dest after sync | Trailing slash mistake | Fix `src/` vs `src`; re-run |
| Deleted production files | `--delete` wrong direction | Restore; receiver is last argument |
| Permission denied | UID mismatch; non-root `-a` | `--rsync-path="sudo rsync"` or align ownership |
| All files re-copied | Clock skew; ownership | `-c`; fix NTP; `--no-owner` if intentional |
| SSH hangs | Firewall; wrong key | `ssh -v`; BatchMode |

## Real-World Applications

Nightly mirrors, artifact deploys over SSH, and checksum dry-runs before cutover ([[diff]] complement).

**Example:** Quiesce or snapshot databases before rsyncing data directories — live DB files without a consistent snapshot risk corruption.

## Pros/Cons or Trade-offs

- **Pro:** Efficient deltas, rich metadata flags, works over SSH with one boring path.
- **Con:** Not bidirectional; many small files over high latency can lose to tar+ssh streams.

## Comparison

- vs `scp`: whole-file copy each time; rsync deltas and mirrors.
- vs Syncthing/git: those handle conflict-aware sync; rsync is last-writer-wins push/pull.

## Mistakes to Avoid

- `--delete` with reversed paths — wipes the wrong side.
- Cron mirrors without a prior `-n` review.
- NFS + `-a` across UID domains without `--numeric-ids`.
- `-z` on a saturated 10G LAN where CPU costs more than bandwidth.
