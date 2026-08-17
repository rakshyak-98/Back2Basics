[[NodeJS]] [[Stream/pipe]] [[Buffers]] [[Stream Events]] [[Stream/stream error]]

# Stream

> Process data in chunks — don’t load the whole file/response into RAM; backpressure keeps readers and writers in pace.

```txt
        Stream ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Stream** to check whether you can explain the mechanism in…

## Sources
- [Node.js — Stream](https://nodejs.org/api/stream.html) — deep-dive
- [Wikipedia — Stream](https://en.wikipedia.org/wiki/Stream) — overview

## Key Concepts
- **Readable / Writable:** Source / sink — File, socket, HTTP body are streams.
- **Duplex / Transform:** Both ways / map chunks — zlib is a Transform.
- **Backpressure:** Slow consumer signals pause
- **highWaterMark:** Buffer size before pause — Tune for throughput vs memory.

## Technical Details
```txt
Readable ──chunk──► Writable
   ▲ highWaterMark buffer
   └── pause when writable is full
```

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

## Mistakes to Avoid
- **Mistake:** **`pipe` doesn’t propagate errors well** — use `stream.pipeline`
- **Mistake:** **Forgot `error` handler** — process can crash on `EPIPE`
- **Mistake:** **Memory climbs:** check Buffering whole body
- **Mistake:** **Hang / never ends:** check Missing `end` / error swallow
- **Mistake:** **Truncated file:** check Error mid-pipe ignored
- **Mistake:** **Slow consumer OOM:** check Ignoring `write` false

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Process data in chunks — don’t load the whole file/response into RAM; backpressu…).
- **Con / when not:** **Tiny payloads already in memory**
- **Con / when not:** **Random access DB rows** — not a byte stream problem.

## Comparison
- vs [[Stream/pipe]]: know when each applies


### Use cases
- In production APIs and tooling, **Stream** shows up whenever teams ship Node/…
