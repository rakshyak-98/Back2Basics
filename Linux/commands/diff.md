[[rsync]] [[Scripting]] [[Linux file management]]

# diff

> diff compares files or trees line-by-line — verify deploy artifacts and config drift before rsync or rollback.





## Interview Relevance
Know `diff -u` for patches, `diff -rq` for trees, and that content-identical ≠ same metadata (use rsync checksum dry-run).

## Sources
- [diff(1)](https://man7.org/linux/man-pages/man1/diff.1.html) — deep-dive
- [GNU Diffutils](https://www.gnu.org/software/diffutils/manual/) — overview

## Core Definition
`diff` reports line-level deltas between two files. Recursive quiet mode (`-rq`) lists paths that differ in content or presence. Exit 0 means identical (for the comparison mode used).

## Key Concepts
- **`-u`:** Unified diff — patch-friendly.
- **`-rq`:** Recursive quiet summary for directories.
- **Whitespace:** `-w`/`-B` reduce noise on configs.
- **Metadata blind spot:** Owner/mode ignored; rsync can check.
- **Symlinks:** Flags decide follow vs compare as links.

## Technical Details
```bash
diff -rq /etc/nginx/sites-available /backup/nginx-sites

diff -u config.yaml config.yaml.bak > config.patch
patch config.yaml < config.patch

diff -uBw old new
diff -u /var/lib/app/state.json{,.bak}

rsync -avnc --delete dir1/ dir2/

if diff -rq "$EXPECTED" "$DEPLOYED" >/dev/null; then
  echo "OK: trees match"
else
  diff -rq "$EXPECTED" "$DEPLOYED"
  exit 1
fi
```

| Symptom | Check | Fix |
|---------|-------|-----|
| “Identical” but perms differ | Metadata | `rsync -avnc` / `stat` |
| Noisy whitespace diffs | Formatting | `-w`/`-B` or normalize |
| Symlink false match | Follow behavior | Check `-N` / symlink flags |
| Huge binary files | Not line-oriented | checksum/`cmp` |

## Real-World Applications
Confirming a config rollback matches backup, generating a reviewable patch, and CI checks that deployed trees match golden artifacts.

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable, patch workflow.
- **Con:** Weak on binaries/metadata; recursive on huge trees is slow.
- **Trade-off:** Quick `diff -rq` vs authoritative `rsync -c` dry-run.

## Comparison
vs [[rsync]]: sync engine with checksum/metadata awareness. vs `cmp`: byte identity without nice diffs. vs git diff: VCS-aware history.

## Mistakes to Avoid
- Treating content-identical as fully equivalent for security-sensitive perms.
- Patching without reviewing unified context.
- Diffing minified/generated blobs instead of sources.
