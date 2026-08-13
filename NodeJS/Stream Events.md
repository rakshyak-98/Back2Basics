[[NodeJS]] [[Stream]] [[Stream/pipe]] [[Stream/stream error]] [[Buffers]]

# Stream Events

> Stream lifecycle signals — `data`/`end`/`drain`/`error`; flowing vs paused modes decide how you pull chunks.

---

## How it works

```txt
paused: pull via read()
flowing: push via 'data'
write() false → wait 'drain'
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Flowing / paused** | Push vs pull | “Lose data if flowing with no listener.” |
| **Backpressure** | Slow sink signals stop | “Honor `false` from `write`.” |
| **`error`** | Failure anytime | “Always listen — even with pipe.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Lost chunks | Flowing, no `data` handler | Attach listener or stay paused |
| OOM | Ignoring `write` false | Pause + `drain` |
| Crash | No `error` handler | Listen both sides; prefer `pipeline` |
| Hang | Never `end` | Forward `end` / destroy on error |

---


## Gotchas

> [!WARNING]
> **`pipe` error handling is weak** — use [[Stream/pipe]] → `pipeline`.

> [!WARNING]
> **Switching modes accidentally** — adding `data` moves to flowing.

---


## When not to use

- **Manual event wiring for simple copies** — `pipeline` is enough.
- **Tiny in-memory data** — Buffer/string, not streams.

---


## Related

[[Stream]] [[Stream/pipe]] [[Stream/stream error]] [[Buffers]]

## Sources

- [Wikipedia — Stream Events](https://en.wikipedia.org/wiki/Stream_Events)
