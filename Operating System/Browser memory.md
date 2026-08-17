[[Operating System]] [[Heap memory]] [[buffer]] [[RAM and Swap memory]] [[OOM (Linux Out Of Memory)]] [[Inter Process Communication]] [[shared memory]] [[cgroup (Control Group)]] [[Buffer cache]]

# Browser memory

> A browser is a multi-process user-space OS environment — each tab’s JavaScript heap, DOM, GPU buffers, and disk cache compete for the same RAM the kernel tracks in [[RAM and Swap memory]].





## Interview Relevance
Shows you can reason about memory beyond “the JS heap” — multi-process accounting, RSS vs heap snapshots, and how container limits or OOM interact with runaway tabs.

## Sources
- [Chromium — Multi-process Architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/) — overview
- Google developers — Chrome memory tooling — overview
- [Wikipedia — Web browser engine](https://en.wikipedia.org/wiki/Web_browser_engine) — overview

## Key Concepts
- **Process split:** browser, GPU, network, and renderer processes (Chromium-derived).
- **JS heap ≠ total cost:** DOM/layout C++ trees, images/canvas, and caches sit outside heap profilers.
- **Caches:** HTTP/code caches behave like an app-level [[Buffer cache]] with eviction.
- **IPC cost:** [[shared memory]] and pipes between processes ([[Inter Process Communication]]).

## Technical Details
Heavy web apps consume gigabytes across:

- **JavaScript heap** — objects, closures, typed arrays ([[Heap memory]] at user level).
- **DOM / layout** — C++ trees in the renderer.
- **Image and canvas buffers** — large contiguous allocations, sometimes GPU-resident.
- **HTTP cache / code cache** — memory-backed with eviction.
- **Shared memory** — IPC between processes.

When system memory is tight, Linux reclaims page cache and may swap anonymous pages. The browser may discard background tabs or kill renderers before the kernel [[OOM (Linux Out Of Memory)]] killer picks a system daemon — runaway tabs can still trigger global OOM.

```bash
# True RSS (not just JS heap)
ps -o pid,rss,cmd -p PID
cat /proc/PID/smaps_rollup
```

Developer tools (`about:memory`, Performance heap snapshots) measure **JS heap** only.

## Real-World Applications
Kiosk / CI runners cap the whole browser under a [[cgroup (Control Group)]]. Performance budgets track renderer RSS, not only heap snapshots, for SPA and WebAssembly apps.

## Pros/Cons or Trade-offs
- **Pro:** Process isolation limits blast radius of a bad tab.
- **Con:** Duplicated heaps and IPC increase baseline memory vs a single-process model.
- **Trade-off:** large ArrayBuffers / Wasm linear memory bypass typical GC pacing — spikes look like native leaks.

## Comparison
- vs [[Heap memory]]: heap is one allocator arena; browser memory is multi-process + GPU + caches.
- vs [[RAM and Swap memory]]: OS accounting of physical pages vs what DevTools shows.

## Mistakes to Avoid
- Trusting only JS heap snapshots when diagnosing “Chrome ate 8 GB”.
- Assuming navigation frees service-worker and Cache API memory.
- Ignoring cgroup limits in containerized browser automation (Chrome OOMs the pod).
