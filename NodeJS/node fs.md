[[NodeJS]] [[file]] [[fsync]] [[Stream]] [[Operating System/file descriptors]] [[Node.js run as a non-privileged user]]

# node fs

> Node's filesystem API (`node:fs`) — promises for app code, streams for size, sync only at boot; understand flags, modes, and EMFILE limits.

```txt
        node fs ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **node fs** to see if you understand what it does operatio…

## Sources
- [Node.js — File system](https://nodejs.org/api/fs.html) — deep-dive
- [Wikipedia — node fs](https://en.wikipedia.org/wiki/node_fs) — overview

## Key Concepts
- **`node:fs` wraps:** `node:fs` wraps POSIX calls
- **File descriptors:** File descriptors are limited per process (`ulimit -n`)


- **Core:** `node:fs` wraps POSIX calls

## Technical Details
- `node:fs` wraps POSIX calls.
- Three surfaces: **`fs/promises`**, callback **`fs`**, and **`*Sync`**.
- Streams integrate with [[EventEmitter]] for incremental I/O.

```
Small config/read     → readFile / writeFile (promises)
Large/unknown size    → createReadStream / createWriteStream
Directory traversal   → readdir + stat OR fs.walk (Node 20+)
Durability            → write + fsync (see [[fsync]])
```

- File descriptors are limited per process (`ulimit -n`)

### Promises API (default)

```javascript
import {
  readFile, writeFile, mkdir, rename, unlink, stat, access, constants,
} from 'node:fs/promises';

await mkdir('data', { recursive: true });
await writeFile('data/out.json', JSON.stringify(obj), 'utf8');
const buf = await readFile('data/out.json'); // Buffer if no encoding
```

### Open with flags

```javascript
import { open } from 'node:fs/promises';

const fh = await open('log.txt', 'a'); // append
try {
  await fh.write('line\n');
} finally {
  await fh.close();
}
```

| Flag | Meaning |
|------|---------|
| `r` | Read (default) |
| `w` | Write, truncate |
| `a` | Append |
| `wx` | Create exclusive (fail if exists) |

### Existence check

```javascript
import { access, constants } from 'node:fs/promises';

try {
  await access('path', constants.R_OK | constants.W_OK);
} catch (e) {
  if (e.code === 'ENOENT') { /* missing */ }
}
```

### Copy / move

```javascript
import { copyFile, rename } from 'node:fs/promises';

await copyFile('src', 'dest', constants.COPYFILE_EXCL); // fail if dest exists
await rename('tmp', 'final'); // atomic on same filesystem
```

### Recursive delete (Node 14.14+)

```javascript
import { rm } from 'node:fs/promises';
await rm('dir', { recursive: true, force: true });
```

### Watch (dev tooling)

```javascript
import { watch } from 'node:fs';
const watcher = watch('.', { recursive: true }, (event, filename) => {
  console.log(event, filename);
});
```

## Mistakes to Avoid
- **Mistake:** **Sync methods block the event loop**
- **Mistake:** **`fs.watch` is unreliable on some OS**
- **Mistake:** **Cross-device rename fails** — copy + unlink instead
- **Mistake:** **`EMFILE: too many open files`:** check `lsof -p PID \
- **Mistake:** **`EACCES` / `EPERM`:** check User, SELinux, mount ro
- **Mistake:** **`EBUSY` on unlink (Windows):** check File still open
- **Mistake:** **`ENOSPC`:** check Disk full
- **Mistake:** **Silent data loss on crash:** check No fsync
- **Mistake:** **Wrong line endings:** check CRLF vs LF

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node's filesystem API (`node:fs`) — promises for app code, streams for size, syn…).
- **Con / when not:** **Object storage at scale**
- **Con / when not:** **Database as file store**

## Comparison
- vs [[file]]: know when each applies


### Use cases
- In production APIs and tooling, **node fs** shows up whenever teams ship Node…
