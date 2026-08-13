[[Operating System]] [[Heap memory]] [[buffer]] [[RAM and Swap memory]] [[OOM (Linux Out Of Memory)]]

# Browser memory

> A browser is a multi-process user-space operating environment — each tab’s JavaScript heap, DOM, GPU buffers, and disk cache compete for the same machine RAM the kernel accounts in [[RAM and Swap memory]].

Chromium-derived browsers split **browser**, **GPU**, **network**, and **renderer** processes. A heavy web app can consume gigabytes across:

- **JavaScript heap** — objects, closures, typed arrays ([[Heap memory]] semantics at user level).
- **DOM / layout** — C++ trees in the renderer, not visible to JS heap profilers alone.
- **Image and canvas buffers** — large contiguous allocations, sometimes GPU-resident.
- **HTTP cache / code cache** — memory-backed with eviction policies similar to [[Buffer cache]].
- **Shared memory** — IPC between processes ([[Inter Process Communication]], [[shared memory]]).

## Pressure and failure

When system memory is tight, Linux reclaims page cache and may swap anonymous pages. The browser may discard tab backgrounds or kill renderer processes before the kernel’s [[OOM (Linux Out Of Memory)]] killer selects a system daemon — but runaway tabs can still trigger global OOM.

Developer tools (`about:memory`, Performance heap snapshots) measure **JS heap** only; use OS tools (`ps`, `smem`, `/proc/PID/smaps_rollup`) for true RSS.

## Engineering implications

- Large ArrayBuffers and WebAssembly linear memory bypass typical GC pacing — spikes look like native leaks.
- Service workers and caches persist across navigations; memory is not freed on `location.href` alone.
- Container limits ([[cgroup (Control Group)]]) cap entire browser cgroup RSS for kiosk or CI runners.

## Sources

- Chromium design docs — [Multi-process Architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/)
- Google developers — memory tooling for Chrome
- Wikipedia: [Web browser engine](https://en.wikipedia.org/wiki/Web_browser_engine)
