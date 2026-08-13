[[commands]] [[rsync]]

# zip

> zip packs files into a portable `.zip` archive — common for sharing; not the best long-term backup format.

---

## How it works

```txt
dirs/files ──► zip -r archive.zip ──► .zip
                     ↑ update / -x exclude
.git tree ──► git archive -o out.zip HEAD   (tracked only)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`-r`** | Recurse directories | “Without `-r` you only zip the folder name, not contents.” |
| **`-x`** | Exclude globs | “Drop `node_modules` and `*.log`.” |
| **`-e`** | Encrypt (password) | “Zip crypto is weak — don’t use for secrets at rest.” |
| **`unzip -l`** | List without extract | “Peek before you land a zip bomb.” |
| **`git archive`** | Tracked tree only | “Clean release zip without junk.” |

---


## Configuration and commands

```bash
# Create
zip -r archive.zip source_dir
zip -r out.zip dir1 dir2 -x "*.log" "*.tmp" "excluded_dir/*"
zip -e secret.zip folder/          # password prompt (weak)

# Update / comment
zip existing.zip file1 file2
zip -z archive.zip                 # add archive comment

# Inspect / extract
unzip -l archive.zip
zipinfo -1 archive.zip | wc -l     # file count
unzip archive.zip -d /tmp/out
unzip -j archive.zip               # junk paths (flat)

# Git-tracked only
git archive -o archive.zip HEAD
```

| Tool | Job |
|------|-----|
| `zip` | Create/update |
| `unzip` | Extract/list |
| `zipinfo` | Detailed listing |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty / tiny archive of a folder | Forgot `-r` | `zip -r` |
| Paths wrong on Windows | Absolute paths | zip from parent; prefer relative paths |
| “Need PK compat” errors | Corrupt / partial download | Re-transfer; `unzip -t archive.zip` |
| Permission denied on extract | Target dir perms | `-d` writable path; don’t extract as root into `/` |
| Huge unexpected size | Included build artifacts | `-x` or `git archive` |

---


## Gotchas

> [!WARNING]
> **Zip encryption is not modern crypto** — use age/gpg/openssl for real confidentiality.

> [!WARNING]
> **Symlinks and Unix perms** — zip is lossy vs `tar`; modes and owners often don’t survive round-trip.

> [!WARNING]
> **Zip bombs** — always `unzip -l` / size-check untrusted archives.

---


## When not to use

- **Backups with ownership/ACLs** — `tar` / [[rsync]].
- **Incremental sync** — [[rsync]].
- **Secrets** — [[gpg]] or age, not `zip -e`.

---


## Related

[[rsync]] [[gpg]] [[Find command]] [[commands]]

## Sources

- [Wikipedia — zip](https://en.wikipedia.org/wiki/zip)
