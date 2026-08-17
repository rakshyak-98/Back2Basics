[[NodeJS]] [[node fs]] [[Buffers]] [[Stream]] [[fsync]] [[Node.js run as a non-privileged user]]

# Node.js `file` module patterns

> Node.js `file` module patterns — node has no separate file package — file I/O lives in node:fs. Three API surfaces:

```txt
        Node.js `file` mod ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js `file` module patterns** to see if you understan…

## Sources
- [Wikipedia — file](https://en.wikipedia.org/wiki/file) — overview

## Key Concepts
- **Node has:** Node has no separate `file` package
- **Small files:** Small files: `readFile` / `writeFile`
- **Without encoding:** Without encoding, `readFile` returns a **Buffer** (binary-safe)


- **Core:** Node has no separate `file` package

## Technical Details
- Node has no separate `file` package — file I/O lives in **`node:fs`**.
- Three API surfaces:

```
fs/promises (async/await)  ← default for app code
fs (callback)              ← legacy; still used by streams
fs sync (*Sync)            ← boot/config only; blocks event loop
```

- Small files: `readFile` / `writeFile`.
- Large files or unknown size: **streams** (`createReadStream`).
- Directory listing: `readdir` with `{ withFileTypes: true }` for type informat…

- Without encoding, `readFile` returns a **Buffer** (binary-safe).
- With `'utf8'`, returns string.

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

## Mistakes to Avoid
- **Mistake:** **`existsSync` + `readFile` race**
- **Mistake:** **Sync fs in request handlers**
- **Mistake:** **Default encoding is UTF-8 in promises API**
- **Mistake:** **`ENOENT` on read:** check Path cwd-relative vs absolute
- **Mistake:** **Garbled text:** check Missing encoding
- **Mistake:** **Event loop stalls:** check Sync `readFileSync` on MB files
- **Mistake:** **`EACCES` / `EPERM`:** check File owner, container user
- **Mistake:** **Partial write after crash:** check Direct overwrite
- **Mistake:** **Buffer vs string confusion:** check No encoding arg

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js `file` module patterns — node has no separate file package — file I/O li…).
- **Con / when not:** **User uploads at scale**
- **Con / when not:** **Watching many files**

## Comparison
- vs [[node fs]]: know when each applies


### Use cases
- In production APIs and tooling, **file** shows up whenever teams ship Node/JS…
