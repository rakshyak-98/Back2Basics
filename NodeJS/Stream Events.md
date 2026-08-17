[[NodeJS]] [[Stream]] [[Stream/pipe]] [[Stream/stream error]] [[Buffers]]

# Stream Events

> Stream lifecycle signals — `data`/`end`/`drain`/`error`; flowing vs paused modes decide how you pull chunks.





## Interview Relevance
Interviewers use **Stream Events** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Flowing / paused**, **Backpressure**, **`error`**.

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

## Real-World Applications
In production APIs and tooling, **Stream Events** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`pipe` error handling is weak** — use [[Stream/pipe]] → `pipeline`; **Switching modes accidentally** — adding `data` moves to flowing.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Stream lifecycle signals — `data`/`end`/`drain`/`error`; flowing vs paused modes…).
- **Con / when not:** **Manual event wiring for simple copies** — `pipeline` is enough.
- **Con / when not:** **Tiny in-memory data** — Buffer/string, not streams.

## Comparison
vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[Stream/pipe]]: know when each applies — do not treat them as interchangeable. vs [[Stream/stream error]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`pipe` error handling is weak** — use [[Stream/pipe]] → `pipeline`.
- **Switching modes accidentally** — adding `data` moves to flowing.
- **Lost chunks:** check Flowing, no `data` handler; fix: Attach listener or stay paused
- **OOM:** check Ignoring `write` false; fix: Pause + `drain`
- **Crash:** check No `error` handler; fix: Listen both sides; prefer `pipeline`
- **Hang:** check Never `end`; fix: Forward `end` / destroy on error
