[[NodeJS]] [[Stream]] [[Stream Events]] [[Stream/stream error]]

# pipe

> Connect readable → writable — `readable.pipe(writable)` moves chunks and applies backpressure; prefer `pipeline` for errors.

---

## How it works

```txt
ReadStream ──pipe──► Transform ──pipe──► WriteStream
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **pipe** | Link streams | “Backpressure included.” |
| **pipeline** | pipe + error cleanup | “Destroys all streams on failure.” |
| **Chain** | Multi-step | “compress then write.” |


## Configuration and commands

```js
import fs from 'node:fs'
import zlib from 'node:zlib'
import { pipeline } from 'node:stream/promises'

await pipeline(
  fs.createReadStream('in.txt'),
  zlib.createGzip(),
  fs.createWriteStream('out.txt.gz'),
)
```

```js
// HTTP: stream a file
fs.createReadStream('index.html').pipe(res)
```

| Knob | Why it matters |
|------|----------------|
| `pipeline` | Error + destroy |
| Transform mid-chain | Compress/encrypt |
| `end: false` option | Keep writable open |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Process crash | Unhandled stream `error` | `pipeline` or `.on('error')` |
| Truncated output | Mid-pipe error ignored | Destroy both; don’t ignore |
| Hang | Consumer never drains | Check backpressure / end |
| Wrong API | Typo `createReadStrema` | Fix method name |

---


## Gotchas

> [!WARNING]
> **`pipe` does not forward errors well** — always prefer `pipeline`.

> [!WARNING]
> **`.pipe(writable).on('error')` only listens on the last return** — attach to each stream or use `pipeline`.

---


## When not to use

- **ObjectMode graphs needing custom control** — manual `write`/`drain` may be clearer.
- **Already-buffered tiny payloads** — skip streams.

---


## Related

[[Stream]] [[Stream Events]] [[Stream/stream error]] [[Buffers]]

## Sources

- [Wikipedia — pipe](https://en.wikipedia.org/wiki/pipe)
