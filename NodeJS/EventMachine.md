[[NodeJS]] [[Event Loop]] [[Node events driven]] [[EventEmitter]]

# EventMachine

> Ruby’s reactor for non-blocking network I/O — same idea as Node’s event loop: one thread, callbacks on readiness.





## Interview Relevance
Interviewers use **EventMachine** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Reactor**, **vs threads**.

## Sources
- [Wikipedia — EventMachine](https://en.wikipedia.org/wiki/EventMachine) — overview

## Key Concepts
- **Reactor:** Single-thread event demux — Like Node’s loop / Netty.
- **vs threads:** Callbacks vs locks — Scale connections without sync hell.

## Technical Details
```txt
Reactor ── select/epoll ──► callback (read/write/timer)
```

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

## Real-World Applications
In production APIs and tooling, **EventMachine** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Blocking in a callback blocks everyone** — same rule as Node’s event loop; **Ruby ecosystem note** — modern Ruby often uses Async/Fiber; EM is legacy in many shops.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Ruby’s reactor for non-blocking network I/O — same idea as Node’s event loop: on…).
- **Con / when not:** **New Node services** — use Node’s loop / [[EventEmitter]], not EM.
- **Con / when not:** **CPU-heavy workers** — processes/threads, not a network reactor.

## Comparison
vs [[Event Loop]]: know when each applies — do not treat them as interchangeable. vs [[Node events driven]]: know when each applies — do not treat them as interchangeable. vs [[EventEmitter]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Blocking in a callback blocks everyone** — same rule as Node’s event loop.
- **Ruby ecosystem note** — modern Ruby often uses Async/Fiber; EM is legacy in many shops.
- **Stalls all clients:** check Blocking work in callback; fix: Defer CPU / use async APIs
- **Port bind fail:** check Already listening; fix: Free port or reuse flag
- **Leaked runs:** check Nested `EM.run`; fix: One reactor per process
