[[management]] [[file mount]] [[rsync]] [[Find command]]

# Linux file management

> File management is create/find/move/permission/backup of data on disk — paths, ownership, and mounts matter more than fancy tools.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** inode + path + mode + owner; tools change those safely; backups need consistent views.

```txt
path → dentry → inode → data blocks
chmod/chown/rm/mv operate on that graph
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **inode** | File metadata object | “Hard links share an inode.” |
| **mode** | rwx bits / ACL | “`stat` before chmod 777.” |
| **mtime/ctime** | Content vs metadata time | “rsync -a preserves mtime.” |
| **sparse** | Holes in files | “Copy tools may expand them.” |
| **atomic replace** | write temp + rename | “Readers never see half files.” |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Disk full | `df -h`; `du -x` | Clear logs; expand volume |
| Permission denied | `namei -l` / `stat` | Fix owner/mode/ACL |
| Vanished files | Wrong mount / overlay | `findmnt`; check bind mounts |
| Copy slow | Many small files | tar stream; tune rsync |

---

## Gotchas

> [!WARNING]
> **`rm -rf` with variable paths** — echo first; prefer trash in interactive use.

> [!WARNING]
> **Crossing bind mounts** with naive `rm`/`chmod -R` can hit the wrong tree.

---

## When NOT to use

- **Database files live** — snapshot/quiesce; don’t raw-copy.
- **Secrets distribution** — use a secrets manager, not world-readable shares.

---

## Related

[[Find command]] [[rsync]] [[file mount]] [[lsof]]
