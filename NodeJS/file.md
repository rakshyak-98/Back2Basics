[[NodeJS]] [[node fs]] [[Buffers]] [[Stream]] [[fsync]] [[Node.js run as a non-privileged user]]

# Node.js `file` module patterns

> Node.js `file` module patterns — node has no separate file package — file I/O lives in node:fs. Three API surfaces:

## Interview Relevance

Interviewers probe **Node.js `file` module patterns** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — file](https://en.wikipedia.org/wiki/file) — overview

## Core Definition

Node has no separate `file` package — file I/O lives in **`node:fs`**. Three API surfaces:

## Key Concepts

- Node has no separate `file` package — file I/O lives in **`node:fs`**. Three API surfaces:
- Small files: `readFile` / `writeFile`. Large files or unknown size: **streams** (`createReadStream`). Directory listing: `readdir` with `{ withFileTypes: true }` for type inform…
- Without encoding, `readFile` returns a **Buffer** (binary-safe). With `'utf8'`, returns string.

## Technical Details

Node has no separate `file` package — file I/O lives in **`node:fs`**. Three API surfaces:

```
fs/promises (async/await)  ← default for app code
fs (callback)              ← legacy; still used by streams
fs sync (*Sync)            ← boot/config only; blocks event loop
```

Small files: `readFile` / `writeFile`. Large files or unknown size: **streams** (`createReadStream`). Directory listing: `readdir` with `{ withFileTypes: true }` for type information without extra `stat` calls.

Without encoding, `readFile` returns a **Buffer** (binary-safe). With `'utf8'`, returns string.

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

## Real-World Applications

In production APIs and tooling, **file** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`existsSync` + `readFile` race** — file can disappear between calls; handle `ENOENT` on open; **Sync fs in request handlers** — one slow disk read blocks all HTTP clients on that process.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Node.js `file` module patterns — node has no separate file package — file I/O li…).
- **Con / when not:** **User uploads at scale** — stream to object storage (S3), don't buffer whole file in RAM.
- **Con / when not:** **Watching many files** — use `fs.watch`/`chokidar` note separately; polling is expensive.

## Comparison

vs [[node fs]]: know when each applies — do not treat them as interchangeable. vs [[Buffers]]: know when each applies — do not treat them as interchangeable. vs [[Stream]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`existsSync` + `readFile` race** — file can disappear between calls; handle `ENOENT` on open.
- **Sync fs in request handlers** — one slow disk read blocks all HTTP clients on that process.
- **Default encoding is UTF-8 in promises API** — binary files need no encoding (Buffer).
- **`ENOENT` on read:** check Path cwd-relative vs absolute; fix: `path.resolve`; log `process.cwd()`
- **Garbled text:** check Missing encoding; fix: Pass `'utf8'`; detect BOM
- **Event loop stalls:** check Sync `readFileSync` on MB files; fix: Switch to promises/streams
- **`EACCES` / `EPERM`:** check File owner, container user; fix: Run as correct UID; fix `chmod`/`chown`
- **Partial write after crash:** check Direct overwrite; fix: Atomic write via temp + rename
- **Buffer vs string confusion:** check No encoding arg; fix: Explicit `'utf8'` or keep Buffer
