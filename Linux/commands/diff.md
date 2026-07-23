[[rsync]] [[Scripting]] [[Linux file management]]

# diff

> One-line: **line and tree comparison** — verify deploy artifacts, config drift, and "are these dirs actually the same?" before rsync or rollback decisions.

## Mental model

`diff` compares **file contents line-by-line** (default unified output). For directories, combine `-r` with `-q` for a fast "any difference?" answer. Exit code matters in scripts: `0` = identical, `1` = different, `2` = error.

```
diff fileA fileB     → line-level delta
diff -rq dir1 dir2   → only names that differ (content or presence)
rsync -avnc          → checksum-level dry-run (heavier, authoritative for sync)
```

| Mode | Command | When |
|------|---------|------|
| Quick dir sameness | `diff -rq dir1 dir2` | Pre/post deploy sanity |
| Readable patch | `diff -u old new` | Review before apply |
| Side-by-side | `diff -y file1 file2` | Human scan |
| Binary | `diff -q a.bin b.bin` | Don't dump hex to terminal |

## Standard config / commands

```bash
# Two directories — only report if different (silent = identical)
diff -rq /etc/nginx/sites-available /backup/nginx-sites
# -q quiet summary  -r recursive

# Unified diff (patch-friendly)
diff -u config.yaml config.yaml.bak > config.patch
patch config.yaml < config.patch

# Ignore whitespace (noisy configs)
diff -uBw old new

# Compare single files with context
diff -u /var/lib/app/state.json{,.bak}

# When diff says "differ" but sizes look same — checksum via rsync dry-run
rsync -avnc --delete dir1/ dir2/
# -n dry-run  -c checksum compare (slower, catches same-size diffs)
```

**In CI/deploy scripts:**

```bash
if diff -rq "$EXPECTED" "$DEPLOYED" >/dev/null; then
  echo "OK: trees match"
else
  diff -rq "$EXPECTED" "$DEPLOYED"
  exit 1
fi
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `diff -rq` silent but apps behave differently | Symlinks, permissions, xattrs | `diff -rqN` or `rsync -avnc`; compare `stat` |
| Huge diff noise | CRLF vs LF | `dos2unix`; `diff -u --strip-trailing-cr` |
| "Only in dir1" spam | Extra files in deploy | `--exclude` patterns; clean staging dir |
| Binary files mess terminal | Used diff without `-q` | `diff -q` or `cmp -s` |
| diff says same, rsync transfers | Timestamp-only change | Expected; use `rsync -c` if content matters |

## Gotchas

> [!WARNING]
> **`diff -rq` compares content, not metadata** — same bytes, different owner/mode still "identical" to diff. Use `rsync -a` preview for permission drift.

> [!WARNING]
> **Symlinks** — default follows symlinks; `-N` treats symlinks as symlinks. Wrong flag → false "identical".

- **Order in `diff -u A B`** — patch applies as "change A into B"; reversing order inverts patch.
- **Large trees** — `diff -rq` still reads every file; for TB-scale use `rsync -avnc` or dedicated tools.

## When NOT to use

- **Live DB row comparison** — export and use SQL/`md5sum` on dumps, not diff on running files.
- **Semantic JSON/YAML equivalence** — key order differs; use `jq -S` normalize or structural diff tools.

## Related

[[rsync]] [[Scripting]] [[Linux file management]]
