[[NodeJS]] [[worker threads]] [[child process]] [[clustering]] [[Optimization]]

# worker (worker threads)

> Run JS on extra OS threads inside one process — good for CPU-bound work without blocking the event loop.

## Interview Relevance

Interviewers use **worker (worker threads)** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Worker**, **postMessage**, **vs child_process**.

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

## Real-World Applications

In production APIs and tooling, **worker** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **I/O-bound APIs don’t need workers** — async I/O already overlaps on the loop; **Don’t share mutable objects** — only `SharedArrayBuffer` is shared memory; everything else is copied/transferred.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Run JS on extra OS threads inside one process — good for CPU-bound work without …).
- **Con / when not:** **Scale HTTP across cores** — [[clustering]] / multiple processes often clearer.
- **Con / when not:** **Run untrusted code** — process isolation + sandbox, not a worker.

## Comparison

vs [[worker threads]]: know when each applies — do not treat them as interchangeable. vs [[child process]]: Child process = separate memory/OS process; worker_threads share some memory via SharedArrayBuffer/MessageChannel. vs [[clustering]]: Workers share process/memory options inside one OS process; cluster forks processes for multi-core HTTP.

## Mistakes to Avoid

- **I/O-bound APIs don’t need workers** — async I/O already overlaps on the loop.
- **Don’t share mutable objects** — only `SharedArrayBuffer` is shared memory; everything else is copied/transferred.
- **Main still blocked:** check Work not in worker; fix: Move CPU loop into worker file
- **Clone errors:** check Non-cloneable values; fix: Transfer buffers; send plain data
- **Memory blow-up:** check Too many workers; fix: Cap pool size to CPU count
- **Crash kills all?:** check Same process; fix: Critical isolation → `child_process`
