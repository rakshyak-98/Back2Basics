[[rsync]] [[Scripting]] [[Linux file management]]

# diff

> diff compares files or trees line-by-line — verify deploy artifacts and config drift before rsync or rollback.

```txt
        diff ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Know `diff -u` for patches, `diff -rq` for trees, and that content-identical …

## Sources
- [diff(1)](https://man7.org/linux/man-pages/man1/diff.1.html) — deep-dive
- [GNU Diffutils](https://www.gnu.org/software/diffutils/manual/) — overview

## Key Concepts
- **`-u`:** Unified diff — patch-friendly.
- **`-rq`:** Recursive quiet summary for directories.
- **Whitespace:** `-w`/`-B` reduce noise on configs.
- **Metadata blind spot:** Owner/mode ignored; rsync can check.
- **Symlinks:** Flags decide follow vs compare as links.


- **Core:** `diff` reports line-level deltas between two files

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

## Mistakes to Avoid
- **Mistake:** Treating content-identical as fully equivalent for security-sens…
- **Mistake:** Patching without reviewing unified context
- **Mistake:** Diffing minified/generated blobs instead of sources

## Pros/Cons or Trade-offs
- **Pro:** Universal, scriptable, patch workflow.
- **Con:** Weak on binaries/metadata; recursive on huge trees is slow.
- **Trade-off:** Quick `diff -rq` vs authoritative `rsync -c` dry-run.

## Comparison
- vs [[rsync]]: sync engine with checksum/metadata awareness


### Use cases
- Confirming a config rollback matches backup, generating a reviewable patch, a…
