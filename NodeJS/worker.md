[[NodeJS]] [[worker threads]] [[child process]] [[clustering]] [[Optimization]]

# worker (worker threads)

> Run JS on extra OS threads inside one process — good for CPU-bound work without blocking the event loop.

```txt
        worker (worker thr ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **worker (worker threads)** to check whether you can explain…

## Sources
- [Node.js — Worker threads](https://nodejs.org/api/worker_threads.html) — deep-dive
- [Wikipedia — worker](https://en.wikipedia.org/wiki/worker) — overview

## Key Concepts
- **Worker:** Extra thread + own V8 — Parallelize CPU; still one machine.
- **postMessage:** Structured clone / transfer — Transfer ArrayBuffers zero-copy.
- **vs child_process:** Threads vs processes — Workers share optional SAB; processes isolate crashes.

## Technical Details
```txt
main ──postMessage──► Worker (V8 isolate)
       ◄──result────
```

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

## Mistakes to Avoid
- **Mistake:** **I/O-bound APIs don’t need workers**
- **Mistake:** **Don’t share mutable objects**
- **Mistake:** **Main still blocked:** check Work not in worker
- **Mistake:** **Clone errors:** check Non-cloneable values
- **Mistake:** **Memory blow-up:** check Too many workers
- **Crash kills all?:** check Same process::** → `child_process`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Run JS on extra OS threads inside one process — good for CPU-bound work without …).
- **Con / when not:** **Scale HTTP across cores**
- **Con / when not:** **Run untrusted code**

## Comparison
- vs [[worker threads]]: know when each applies


### Use cases
- In production APIs and tooling, **worker** shows up whenever teams ship Node/…
