[[NodeJS]] [[Stream]] [[Stream/pipe]] [[Stream Events]] [[Buffers]]

# stream error

> Stream failures — wrong chunk types, missing `pipeline` callback, and unclean destroy; handle `error` or use `stream/promises`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Writable wants string/Buffer/Uint8Array (unless `objectMode`). Callback-style `pipeline` needs a final function; promise API does not.

```txt
bad: Readable.from(alreadyBuffer) mistyped / number chunk
bad: pipeline(a,b,ws) without callback → treats WriteStream as fn
good: pipeline from 'stream/promises' or callback last
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ERR_INVALID_ARG_TYPE** | Wrong pipeline args | “Forgot callback or used wrong import.” |
| **chunk type** | Must be Buffer/string | “Don’t write raw numbers.” |
| **destroy** | Tear down on error | “pipeline does this for you.” |

## Standard config / commands

```js
import { pipeline } from 'node:stream/promises'
import fs from 'node:fs'
import zlib from 'node:zlib'

await pipeline(
  fs.createReadStream(file),
  zlib.createGzip(),
  fs.createWriteStream(file + '.gz'),
)

// Already a Buffer — don’t wrap wrong:
// Readable.from([file.buffer]) or PassThrough end(buffer)
```

| Knob | Why it matters |
|------|----------------|
| `stream/promises` | No callback footgun |
| `objectMode` | Allow non-Buffer chunks |
| `error` listeners | Required if not using pipeline |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| chunk must be string/Buffer | Wrote number/object | Buffer/string or `objectMode` |
| streams[last] must be function | Callback `pipeline` sans cb | Add cb or use promises API |
| Socket left open | Raw `pipe` + error | `pipeline` |
| Readable.from(Buffer) odd | API expects iterable | `Readable.from([buf])` or `.end(buf)` |

---

## Gotchas

> [!WARNING]
> **Two `pipeline` APIs** — `require('stream').pipeline` needs callback; `stream/promises` returns a Promise.

> [!WARNING]
> **Unhandled `error`** — can abort the process.

---

## When NOT to use

- **Happy-path only demos** — still add error paths before prod.

---

## Related

[[Stream]] [[Stream/pipe]] [[Stream Events]] [[Buffers]]
