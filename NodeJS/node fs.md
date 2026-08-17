[[NodeJS]] [[file]] [[fsync]] [[Stream]] [[Operating System/file descriptors]] [[Node.js run as a non-privileged user]]

# node fs

> Node's filesystem API (`node:fs`) — promises for app code, streams for size, sync only at boot; understand flags, modes, and EMFILE limits.





## Interview Relevance
Interviewers probe **node fs** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Node.js — File system](https://nodejs.org/api/fs.html) — deep-dive
- [Wikipedia — node fs](https://en.wikipedia.org/wiki/node_fs) — overview

## Core Definition
`node:fs` wraps POSIX calls. Three surfaces: **`fs/promises`**, callback **`fs`**, and **`*Sync`**. Streams integrate with [[EventEmitter]] for incremental I/O.

## Key Concepts
- `node:fs` wraps POSIX calls. Three surfaces: **`fs/promises`**, callback **`fs`**, and **`*Sync`**. Streams integrate with [[EventEmitter]] for incremental I/O.
- File descriptors are limited per process (`ulimit -n`); leaking watchers or handles causes `EMFILE`.

## Technical Details
`node:fs` wraps POSIX calls. Three surfaces: **`fs/promises`**, callback **`fs`**, and **`*Sync`**. Streams integrate with [[EventEmitter]] for incremental I/O.

```
Small config/read     → readFile / writeFile (promises)
Large/unknown size    → createReadStream / createWriteStream
Directory traversal   → readdir + stat OR fs.walk (Node 20+)
Durability            → write + fsync (see [[fsync]])
```

File descriptors are limited per process (`ulimit -n`); leaking watchers or handles causes `EMFILE`.

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

## Real-World Applications
In production APIs and tooling, **node fs** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Sync methods block the event loop** — `readFileSync` in HTTP handlers freezes all clients; **`fs.watch` is unreliable on some OS** — debounce; use chokidar for production file triggers.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node's filesystem API (`node:fs`) — promises for app code, streams for size, syn…).
- **Con / when not:** **Object storage at scale** — S3/GCS SDK, not local fs on ephemeral disks.
- **Con / when not:** **Database as file store** — use [[GridFS]] or blob storage for large binaries in DB context.

## Comparison
vs [[file]]: know when each applies — do not treat them as interchangeable. vs [[fsync]]: know when each applies — do not treat them as interchangeable. vs [[Stream]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Sync methods block the event loop** — `readFileSync` in HTTP handlers freezes all clients.
- **`fs.watch` is unreliable on some OS** — debounce; use chokidar for production file triggers.
- **Cross-device rename fails** — copy + unlink instead.
- **`EMFILE: too many open files`:** check `lsof -p PID \; fix: wc -l`
- **`EACCES` / `EPERM`:** check User, SELinux, mount ro; fix: Fix ownership; run as correct user
- **`EBUSY` on unlink (Windows):** check File still open; fix: Close handles before delete
- **`ENOSPC`:** check Disk full; fix: Clean logs; rotate before write
- **Silent data loss on crash:** check No fsync; fix: Atomic rename pattern; see [[fsync]]
- **Wrong line endings:** check CRLF vs LF; fix: Normalize on read or use `'utf8'` consistently
