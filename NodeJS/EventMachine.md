<!-- note-strategy: operational -->
[[NodeJS]] [[Event Loop]] [[Node events driven]]

# EventMachine

> Ruby’s reactor for non-blocking network I/O — same idea as Node’s event loop: one thread, callbacks on readiness.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** EventMachine runs a reactor: register sockets/timers, get called when ready — avoid thread-per-connection for high fan-in.

```txt
Reactor ── select/epoll ──► callback (read/write/timer)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Reactor** | Single-thread event demux | “Like Node’s loop / Netty.” |
| **vs threads** | Callbacks vs locks | “Scale connections without sync hell.” |

## Standard config / commands

```ruby
require 'eventmachine'
EventMachine.run do
  EventMachine.start_server '0.0.0.0', 8080, EchoServer
end
```

| Knob | Why it matters |
|------|----------------|
| `EM.run` | Starts reactor; blocks until stop |
| Defer / thread pool | Offload CPU so reactor stays free |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stalls all clients | Blocking work in callback | Defer CPU / use async APIs |
| Port bind fail | Already listening | Free port or reuse flag |
| Leaked runs | Nested `EM.run` | One reactor per process |

---

## Gotchas

> [!WARNING]
> **Blocking in a callback blocks everyone** — same rule as Node’s event loop.

> [!WARNING]
> **Ruby ecosystem note** — modern Ruby often uses Async/Fiber; EM is legacy in many shops.

---

## When NOT to use

- **New Node services** — use Node’s loop / [[EventEmitter]], not EM.
- **CPU-heavy workers** — processes/threads, not a network reactor.

---

## Related

[[Event Loop]] [[Node events driven]] [[EventEmitter]]
