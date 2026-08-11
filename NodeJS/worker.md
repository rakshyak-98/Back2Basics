[[NodeJS]] [[worker threads]] [[child process]] [[clustering]]

# worker (worker threads)

> Run JS on extra OS threads inside one process — good for CPU-bound work without blocking the event loop.

---

## Mental model

**Say it in one breath:** Main thread posts messages to a `Worker`; heavy compute runs off-loop. Not a substitute for multi-machine scale — use for CPU, not for magically more I/O throughput.

```txt
main ──postMessage──► Worker (V8 isolate)
       ◄──result────
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Worker** | Extra thread + own V8 | “Parallelize CPU; still one machine.” |
| **postMessage** | Structured clone / transfer | “Transfer ArrayBuffers zero-copy.” |
| **vs child_process** | Threads vs processes | “Workers share optional SAB; processes isolate crashes.” |

## Standard config / commands

```js
import { Worker } from 'node:worker_threads'

const w = new Worker(new URL('./cpu.js', import.meta.url), { workerData: { n: 40 } })
w.on('message', console.log)
w.on('error', console.error)
```

| Knob | Why it matters |
|------|----------------|
| `workerData` | Init payload |
| Transfer list | Avoid cloning big buffers |
| Pool | Amortize thread startup |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Main still blocked | Work not in worker | Move CPU loop into worker file |
| Clone errors | Non-cloneable values | Transfer buffers; send plain data |
| Memory blow-up | Too many workers | Cap pool size to CPU count |
| Crash kills all? | Same process | Critical isolation → `child_process` |

---

## Gotchas

> [!WARNING]
> **I/O-bound APIs don’t need workers** — async I/O already overlaps on the loop.

> [!WARNING]
> **Don’t share mutable objects** — only `SharedArrayBuffer` is shared memory; everything else is copied/transferred.

---

## When NOT to use

- **Scale HTTP across cores** — [[clustering]] / multiple processes often clearer.
- **Run untrusted code** — process isolation + sandbox, not a worker.

---

## Related

[[worker threads]] [[child process]] [[clustering]] [[Optimization]]
