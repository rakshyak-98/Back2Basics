[[NodeJS]] [[file]] [[fsync]] [[Stream]] [[Operating System/file descriptors]]

# node fs

> One-line: Node's filesystem API (`node:fs`) — promises for app code, streams for size, sync only at boot; understand flags, modes, and EMFILE limits.

## Mental model

`node:fs` wraps POSIX calls. Three surfaces: **`fs/promises`**, callback **`fs`**, and **`*Sync`**. Streams integrate with [[EventEmitter]] for incremental I/O.

```
Small config/read     → readFile / writeFile (promises)
Large/unknown size    → createReadStream / createWriteStream
Directory traversal   → readdir + stat OR fs.walk (Node 20+)
Durability            → write + fsync (see [[fsync]])
```

File descriptors are limited per process (`ulimit -n`); leaking watchers or handles causes `EMFILE`.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EMFILE: too many open files` | `lsof -p PID \| wc -l` | Close streams; raise `ulimit -n`; pool handles |
| `EACCES` / `EPERM` | User, SELinux, mount ro | Fix ownership; run as correct user |
| `EBUSY` on unlink (Windows) | File still open | Close handles before delete |
| `ENOSPC` | Disk full | Clean logs; rotate before write |
| Silent data loss on crash | No fsync | Atomic rename pattern; see [[fsync]] |
| Wrong line endings | CRLF vs LF | Normalize on read or use `'utf8'` consistently |

## Gotchas

> [!WARNING]
> **Sync methods block the event loop** — `readFileSync` in HTTP handlers freezes all clients.

> [!WARNING]
> **`fs.watch` is unreliable on some OS** — debounce; use chokidar for production file triggers.

> [!WARNING]
> **Cross-device rename fails** — copy + unlink instead.

## When NOT to use

- **Object storage at scale** — S3/GCS SDK, not local fs on ephemeral disks.
- **Database as file store** — use [[GridFS]] or blob storage for large binaries in DB context.

## Related

[[file]] [[Stream]] [[fsync]] [[Operating System/file descriptors]] [[Node.js run as a non-privileged user]]
