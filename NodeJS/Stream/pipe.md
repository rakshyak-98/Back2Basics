[[NodeJS]] [[Stream]] [[Stream Events]] [[Stream/stream error]] [[Buffers]]

# pipe

> Connect readable → writable — `readable.pipe(writable)` moves chunks and applies backpressure; prefer `pipeline` for errors.

```txt
        pipe ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **pipe** to check whether you can explain the mechanism in p…

## Sources
- [Node.js — readable.pipe](https://nodejs.org/api/stream.html#readablepipedestination-options) — deep-dive
- [Wikipedia — pipe](https://en.wikipedia.org/wiki/pipe) — overview

## Key Concepts
- **pipe:** Link streams — Backpressure included.
- **pipeline:** pipe + error cleanup — Destroys all streams on failure.
- **Chain:** Multi-step — compress then write.

## Technical Details
```txt
ReadStream ──pipe──► Transform ──pipe──► WriteStream
```

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

## Mistakes to Avoid
- **Mistake:** **`pipe` does not forward errors well**
- **Mistake:** **`.pipe(writable).on('error')` only listens on the last return**
- **Mistake:** **Process crash:** check Unhandled stream `error`
- **Mistake:** **Truncated output:** check Mid-pipe error ignored
- **Mistake:** **Hang:** check Consumer never drains
- **Mistake:** **Wrong API:** check Typo `createReadStrema`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Connect readable → writable — `readable.pipe(writable)` moves chunks and applies…).
- **Con / when not:** **ObjectMode graphs needing custom control**
- **Con / when not:** **Already-buffered tiny payloads** — skip streams.

## Comparison
- vs [[Stream]]: know when each applies


### Use cases
- In production APIs and tooling, **pipe** shows up whenever teams ship Node/JS…
