[[NodeJS]] [[node fs]] [[Buffers]] [[Stream]]

# Node.js `file` module patterns

> One-line: read/write paths via `node:fs` — choose sync vs promise vs stream based on size and startup cost; never block the event loop on large sync I/O.

## Mental model

Node has no separate `file` package — file I/O lives in **`node:fs`**. Three API surfaces:

```
fs/promises (async/await)  ← default for app code
fs (callback)              ← legacy; still used by streams
fs sync (*Sync)            ← boot/config only; blocks event loop
```

Small files: `readFile` / `writeFile`. Large files or unknown size: **streams** (`createReadStream`). Directory listing: `readdir` with `{ withFileTypes: true }` for type info without extra `stat` calls.

Without encoding, `readFile` returns a **Buffer** (binary-safe). With `'utf8'`, returns string.

## Standard config / commands

### Read text file (production default)

```javascript
import { readFile } from 'node:fs/promises';

const data = await readFile('config.json', 'utf8');
const config = JSON.parse(data);
```

### Check existence (prefer access over existsSync in async code)

```javascript
import { access, constants } from 'node:fs/promises';

async function fileExists(path) {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}
```

```javascript
import { existsSync } from 'node:fs';

if (existsSync('./config.yaml')) {
  // OK for sync bootstrap only — race between check and open still possible
}
```

### List directory

```javascript
import { readdir } from 'node:fs/promises';

const entries = await readdir('.', { withFileTypes: true });
for (const ent of entries) {
  console.log(ent.name, ent.isDirectory() ? 'dir' : 'file');
}
```

### Write atomically (crash-safe config)

```javascript
import { writeFile, rename } from 'node:fs/promises';
import { join } from 'node:path';

async function atomicWrite(target, content) {
  const tmp = join(target, `.${Date.now()}.tmp`);
  await writeFile(tmp, content, 'utf8');
  await rename(tmp, target); // same filesystem required
}
```

### Large file — stream

```javascript
import { createReadStream } from 'node:fs';

const reader = createReadStream('large-video.mp4');
reader.on('data', (chunk) => processChunk(chunk));
reader.on('error', (err) => console.error(err));
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ENOENT` on read | Path cwd-relative vs absolute | `path.resolve`; log `process.cwd()` |
| Garbled text | Missing encoding | Pass `'utf8'`; detect BOM |
| Event loop stalls | Sync `readFileSync` on MB files | Switch to promises/streams |
| `EACCES` / `EPERM` | File owner, container user | Run as correct UID; fix `chmod`/`chown` |
| Partial write after crash | Direct overwrite | Atomic write via temp + rename |
| Buffer vs string confusion | No encoding arg | Explicit `'utf8'` or keep Buffer |

## Gotchas

> [!WARNING]
> **`existsSync` + `readFile` race** — file can disappear between calls; handle `ENOENT` on open.

> [!WARNING]
> **Sync fs in request handlers** — one slow disk read blocks all HTTP clients on that process.

> [!WARNING]
> **Default encoding is UTF-8 in promises API** — binary files need no encoding (Buffer).

## When NOT to use

- **User uploads at scale** — stream to object storage (S3), don't buffer whole file in RAM.
- **Watching many files** — use `fs.watch`/`chokidar` note separately; polling is expensive.

## Related

[[node fs]] [[Buffers]] [[Stream]] [[fsync]] [[Node.js run as a non-privileged user]]
