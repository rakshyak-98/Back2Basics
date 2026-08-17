[[NodeJS]] [[Stream]] [[Stream/pipe]] [[Stream/stream error]] [[Buffers]]

# Stream Events

> Stream lifecycle signals — `data`/`end`/`drain`/`error`; flowing vs paused modes decide how you pull chunks.

```txt
        Stream Events ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Stream Events** to check whether you can explain the mecha…

## Sources
- [Node.js — Stream events](https://nodejs.org/api/stream.html#event-data) — deep-dive
- [Wikipedia — Stream Events](https://en.wikipedia.org/wiki/Stream_Events) — overview

## Key Concepts
- **Flowing / paused:** Push vs pull — Lose data if flowing with no listener.
- **Backpressure:** Slow sink signals stop — Honor `false` from `write`.
- **`error`:** Failure anytime — Always listen — even with pipe.

## Technical Details
```txt
paused: pull via read()
flowing: push via 'data'
write() false → wait 'drain'
```

```js
readable.on('data', (chunk) => {
  if (!writable.write(chunk)) readable.pause()
})
writable.on('drain', () => readable.resume())
readable.on('end', () => writable.end())
readable.on('error', handler)
writable.on('error', handler)
```

| Knob | Why it matters |
|------|----------------|
| `pipe` / `pipeline` | Mode + backpressure handled |
| `highWaterMark` | Buffer before pause |
| `for await` | Modern consume without `data` |

## Mistakes to Avoid
- **`pipe` error handling is weak**::** → `pipeline`
- **Mistake:** **Switching modes accidentally** — adding `data` moves to flowing
- **Mistake:** **Lost chunks:** check Flowing, no `data` handler
- **Mistake:** **OOM:** check Ignoring `write` false; fix: Pause + `drain`
- **Mistake:** **Crash:** check No `error` handler
- **Mistake:** **Hang:** check Never `end`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Stream lifecycle signals — `data`/`end`/`drain`/`error`; flowing vs paused modes…).
- **Con / when not:** **Manual event wiring for simple copies**
- **Con / when not:** **Tiny in-memory data** — Buffer/string, not streams.

## Comparison
- vs [[Stream]]: know when each applies


### Use cases
- In production APIs and tooling, **Stream Events** shows up whenever teams shi…
