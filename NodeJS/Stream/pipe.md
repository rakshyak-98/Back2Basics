[[NodeJS]] [[Stream]] [[Stream Events]] [[Stream/stream error]] [[Buffers]]

# pipe

> Connect readable → writable — `readable.pipe(writable)` moves chunks and applies backpressure; prefer `pipeline` for errors.

## Interview Relevance

Interviewers use **pipe** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **pipe**, **pipeline**, **Chain**.

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

## Real-World Applications

In production APIs and tooling, **pipe** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`pipe` does not forward errors well** — always prefer `pipeline`; **`.pipe(writable).on('error')` only listens on the last return** — attach to each stream or use `pipeline`.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Connect readable → writable — `readable.pipe(writable)` moves chunks and applies…).
- **Con / when not:** **ObjectMode graphs needing custom control** — manual `write`/`drain` may be clearer.
- **Con / when not:** **Already-buffered tiny payloads** — skip streams.

## Comparison

vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[Stream Events]]: know when each applies — do not treat them as interchangeable. vs [[Stream/stream error]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`pipe` does not forward errors well** — always prefer `pipeline`.
- **`.pipe(writable).on('error')` only listens on the last return** — attach to each stream or use `pipeline`.
- **Process crash:** check Unhandled stream `error`; fix: `pipeline` or `.on('error')`
- **Truncated output:** check Mid-pipe error ignored; fix: Destroy both; don’t ignore
- **Hang:** check Consumer never drains; fix: Check backpressure / end
- **Wrong API:** check Typo `createReadStrema`; fix: Fix method name
