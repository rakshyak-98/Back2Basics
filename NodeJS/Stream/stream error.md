[[NodeJS]] [[Stream]] [[Stream/pipe]] [[Stream Events]] [[Buffers]]

# stream error

> Stream failures — wrong chunk types, missing `pipeline` callback, and unclean destroy; handle `error` or use `stream/promises`.

```txt
        stream error ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **stream error** to check whether you can explain the mechan…

## Sources
- [Node.js — Stream error handling](https://nodejs.org/api/stream.html#error-handling) — deep-dive
- [Wikipedia — stream error](https://en.wikipedia.org/wiki/stream_error) — overview

## Key Concepts
- **ERR_INVALID_ARG_TYPE:** Wrong pipeline args — Forgot callback or used wrong import.
- **chunk type:** Must be Buffer/string — Don’t write raw numbers.
- **destroy:** Tear down on error — pipeline does this for you.

## Technical Details
```txt
bad: Readable.from(alreadyBuffer) mistyped / number chunk
bad: pipeline(a,b,ws) without callback → treats WriteStream as fn
good: pipeline from 'stream/promises' or callback last
```

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

## Mistakes to Avoid
- **Mistake:** **Two `pipeline` APIs**
- **Mistake:** **Unhandled `error`** — can abort the process
- **Mistake:** **chunk must be string/Buffer:** check Wrote number/object
- **Mistake:** **streams[last] must be function:** check Callback `pipeline` sa…
- **Mistake:** **Socket left open:** check Raw `pipe` + error; fix: `pipeline`
- **Mistake:** **Readable.from(Buffer) odd:** check API expects iterable

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Stream failures — wrong chunk types, missing `pipeline` callback, and unclean de…).
- **Con / when not:** **Happy-path only demos**

## Comparison
- vs [[Stream]]: know when each applies


### Use cases
- In production APIs and tooling, **stream error** shows up whenever teams ship…
