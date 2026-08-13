<!-- note-strategy: operational -->
[[NodeJS]] [[Stream/pipe]] [[Buffers]] [[Stream Events]]

# Stream

> Process data in chunks — don’t load the whole file/response into RAM; backpressure keeps readers and writers in pace.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Readable pulls/pushes chunks; Writable consumes them; `.pipe` / `pipeline` connects them and handles backpressure.

```txt
Readable ──chunk──► Writable
   ▲ highWaterMark buffer
   └── pause when writable is full
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Readable / Writable** | Source / sink | “File, socket, HTTP body are streams.” |
| **Duplex / Transform** | Both ways / map chunks | “zlib is a Transform.” |
| **Backpressure** | Slow consumer signals pause | “Pipe respects it; manual `write` must check return.” |
| **highWaterMark** | Buffer size before pause | “Tune for throughput vs memory.” |

## Standard config / commands

```js
import fs from 'node:fs'
import { pipeline } from 'node:stream/promises'

await pipeline(
  fs.createReadStream('in.bin', { highWaterMark: 64 * 1024 }),
  fs.createWriteStream('out.bin'),
)
```

| Knob | Why it matters |
|------|----------------|
| `pipeline` over raw `pipe` | Forwards errors + destroys streams |
| `objectMode` | Chunks are objects, not Buffers |
| `'data'` vs async iterate | Prefer `for await` / pipeline in modern code |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Memory climbs | Buffering whole body | Stream; don’t `.concat` all chunks |
| Hang / never ends | Missing `end` / error swallow | `pipeline`; listen `error` |
| Truncated file | Error mid-pipe ignored | Destroy both sides on error |
| Slow consumer OOM | Ignoring `write` false | Wait for `drain` |

---

## Gotchas

> [!WARNING]
> **`pipe` doesn’t propagate errors well** — use `stream.pipeline`.

> [!WARNING]
> **Forgot `error` handler** — process can crash on `EPIPE`.

---

## When NOT to use

- **Tiny payloads already in memory** — a Buffer/string is simpler.
- **Random access DB rows** — not a byte stream problem.

---

## Related

[[Stream/pipe]] [[Buffers]] [[Stream Events]] [[Stream/stream error]]
