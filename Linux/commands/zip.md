[[commands]] [[rsync]] [[gpg]] [[Find command]]

# zip

> Packs files into a portable `.zip` archive — common for sharing; lossy for Unix permissions versus `tar`.

```txt
        zip ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Expect `-r` for directories, weak zip encryption vs real crypto, and when to …

## Sources
- [Info-ZIP zip documentation](http://infozip.sourceforge.net/Zip.html) — overview
- [Wikipedia — ZIP (file format)](https://en.wikipedia.org/wiki/ZIP_(file_format)) — overview

## Key Concepts
- **`-r` recurse:** without it you may zip only the directory entry, not contents.
- **`-x` exclude:** drop `node_modules`, logs, build junk.
- **`-e` encrypt:** password zip crypto is weak — not for secrets at rest.
- **`unzip -l`:** list before extract — zip-bomb hygiene.
- **`git archive`:** tracked tree only — clean release zips.

## Technical Details
```txt
dirs/files ──► zip -r archive.zip ──► .zip
.git tree ──► git archive -o out.zip HEAD   (tracked only)
```

```bash
zip -r archive.zip source_dir
zip -r out.zip dir1 dir2 -x "*.log" "*.tmp" "excluded_dir/*"
zip -e secret.zip folder/
zip existing.zip file1 file2
unzip -l archive.zip
zipinfo -1 archive.zip | wc -l
unzip archive.zip -d /tmp/out
unzip -j archive.zip
git archive -o archive.zip HEAD
unzip -t archive.zip
```

| Tool | Job |
|------|-----|
| `zip` | Create/update |
| `unzip` | Extract/list |
| `zipinfo` | Detailed listing |

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty / tiny archive of a folder | Forgot `-r` | `zip -r` |
| Paths wrong on Windows | Absolute paths | Zip from parent; relative paths |
| PK compat errors | Corrupt / partial download | Re-transfer; `unzip -t` |
| Huge unexpected size | Build artifacts included | `-x` or `git archive` |

## Mistakes to Avoid
- **Mistake:** Using `zip -e` for confidential data
- **Mistake:** Extracting untrusted archives without listing size first
- **Mistake:** Relying on zip for backups that need ownership/ACLs

## Pros/Cons or Trade-offs
- **Pro:** Universal interchange format across Windows/macOS/Linux.
- **Con:** Lossy on symlinks/owners/ACLs; encryption is not modern crypto.

## Comparison
- vs `tar`: better Unix metadata fidelity for backups.
- vs [[rsync]]: incremental sync, not a one-shot archive.
- vs [[gpg]]/age: real confidentiality for secrets.


### Use cases
- Shipping a release artifact to non-Unix users, or peeking an untrusted upload…
