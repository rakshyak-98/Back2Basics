[[file mount]] [[rsync]] [[Find command]] [[management/Linux file management]] [[media mount as read only]]

# Linux file management

> Create, find, move, permission, and back up data on disk — paths, ownership, and mounts matter more than fancy tools.

```txt
        Linux file managem ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Everyday ops: inodes/hard links, `stat` before `chmod 777`, `-xdev`, and atom…

## Sources
- `man 1 find`, `man 1 rsync`, `man 2 rename` — deep-dive
- [FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — overview

## Key Concepts
- **inode:** metadata object — hard links share one.
- **mode / ACL:** permission bits; never default to 777.
- **mtime vs ctime:** content vs metadata change times.
- **atomic replace:** write temp + `rename` so readers never see half files.
- **Don’t cross mounts blindly:** `-xdev` / `findmnt`.

## Technical Details
```txt
path → dentry → inode → data blocks
chmod/chown/rm/mv operate on that graph
```

```bash
ls -la
stat file
find /var -xdev -type f -size +1G
du -sh * | sort -h
install -d -m 755 -o app -g app /var/lib/app
rsync -aHAX --delete src/ dst/
```

| Knob | Why it matters |
|------|----------------|
| `-xdev` | Don’t cross mounts in find/du |
| `install` vs `cp` | Mode/owner in one step |

| Symptom | Check | Fix |
|---------|-------|-----|
| Disk full | `df -h`; `du -x` | Clear logs; expand volume |
| Permission denied | `namei -l` / `stat` | Fix owner/mode/ACL |
| Vanished files | Wrong mount / overlay | `findmnt`; check binds |
| Copy slow | Many small files | tar stream; tune rsync |

## Mistakes to Avoid
- **Mistake:** `rm -rf` with unchecked variables
- **Mistake:** Raw-copying live database files without snapshot/quiesce
- **Mistake:** Recursive operations that cross unexpected bind mounts

## Pros/Cons or Trade-offs
- **Pro:** Simple primitives compose into safe deploy/backup workflows.
- **Con:** Recursive chmod/rm across bind mounts can hit the wrong tree.

## Comparison
- vs [[file mount]]: attaching filesystems vs managing files on them.
- vs object storage: different consistency and permission models.


### Use cases
- Reclaim space with `du -x`, move an app tree with `rsync -aHAX`, and create d…
