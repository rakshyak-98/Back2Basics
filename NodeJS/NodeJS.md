[[NodeJS]] [[event emitter]] [[Stream]] [[npm command]] [[expressjs]] [[worker]] [[node modules]]

# NodeJS

> JavaScript runtime built on V8 + libuv — single-threaded event loop for I/O, with threadpool/workers for some blocking work.





## Interview Relevance
Interviewers use **NodeJS** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Event loop**, **libuv**, **Threadpool**.

## Sources
- [Node.js — Introduction](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs) — overview
- [Node.js — API docs](https://nodejs.org/docs/latest/api/) — deep-dive
- [Wikipedia — NodeJS](https://en.wikipedia.org/wiki/NodeJS) — overview

## Key Concepts
- **Event loop:** Schedules callbacks — Non-blocking I/O model.
- **libuv:** C library under Node — FS/DNS/network primitives.
- **Threadpool:** Default 4 threads — Some fs/crypto/dns use it.

## Technical Details
```txt
timers → pending → poll (I/O) → check → close
         ↑______________________________|
```

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

### Where to go next

| Symptom / need | Go to |
|----------------|-------|
| … | [[…]] |

### Related topics in this domain

- …: [[…]]

## Real-World Applications
In production APIs and tooling, **NodeJS** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **“Node is multi-threaded”** — only partially; your JS is not parallel by default; **Unhandled rejections** — treat as fatal in servers.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (JavaScript runtime built on V8 + libuv — single-threaded event loop for I/O, wit…).
- **Con / when not:** **Heavy pure CPU services** — Go/Rust/Java may fit better (or isolate workers).
- **Con / when not:** **Browser-only APIs** — DOM isn’t in Node.

## Comparison
vs [[event emitter]]: know when each applies — do not treat them as interchangeable. vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[npm command]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **“Node is multi-threaded”** — only partially; your JS is not parallel by default.
- **Unhandled rejections** — treat as fatal in servers.
- **All requests slow:** check Sync CPU on loop; fix: Profile; worker
- **Memory climb:** check Leaks / caches; fix: Heap snapshot
- **Weird fs latency:** check Threadpool saturated; fix: Raise size / reduce load
- **Module errors:** check ESM/CJS mix; fix: See [[node modules]]
