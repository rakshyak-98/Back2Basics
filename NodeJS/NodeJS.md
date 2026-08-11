[[NodeJS]] [[event emitter]] [[Stream]] [[npm command]]

# NodeJS

> JavaScript runtime built on V8 + libuv — single-threaded event loop for I/O, with threadpool/workers for some blocking work.

---

## Mental model

**Say it in one breath:** JS runs on one main thread; async I/O callbacks/promises resume on the loop. CPU-heavy work blocks everyone unless moved to [[worker]] / [[child process]].

```txt
timers → pending → poll (I/O) → check → close
         ↑______________________________|
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Event loop** | Schedules callbacks | “Non-blocking I/O model.” |
| **libuv** | C library under Node | “FS/DNS/network primitives.” |
| **Threadpool** | Default 4 threads | “Some fs/crypto/dns use it.” |

## Standard config / commands

```bash
node app.js
node --watch app.js
node -e 'console.log(process.version)'
```

| Knob | Why it matters |
|------|----------------|
| `NODE_OPTIONS` | Shared flags (inspect, max-old-space) |
| `UV_THREADPOOL_SIZE` | More parallel fs/crypto |
| ESM vs CJS | `type: module` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| All requests slow | Sync CPU on loop | Profile; worker |
| Memory climb | Leaks / caches | Heap snapshot |
| Weird fs latency | Threadpool saturated | Raise size / reduce load |
| Module errors | ESM/CJS mix | See [[node modules]] |

---

## Gotchas

> [!WARNING]
> **“Node is multi-threaded”** — only partially; your JS is not parallel by default.

> [!WARNING]
> **Unhandled rejections** — treat as fatal in servers.

---

## When NOT to use

- **Heavy pure CPU services** — Go/Rust/Java may fit better (or isolate workers).
- **Browser-only APIs** — DOM isn’t in Node.

---

## Related

[[event emitter]] [[Stream]] [[expressjs]] [[worker]] [[node modules]]
