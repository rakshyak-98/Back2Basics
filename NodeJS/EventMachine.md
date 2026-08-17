[[NodeJS]] [[Event Loop]] [[Node events driven]] [[EventEmitter]]

# EventMachine

> Ruby’s reactor for non-blocking network I/O — same idea as Node’s event loop: one thread, callbacks on readiness.

```txt
        EventMachine ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **EventMachine** to check whether you can explain the mechan…

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

## Mistakes to Avoid
- **Mistake:** **Blocking in a callback blocks everyone**
- **Mistake:** **Ruby ecosystem note**
- **Mistake:** **Stalls all clients:** check Blocking work in callback
- **Mistake:** **Port bind fail:** check Already listening
- **Mistake:** **Leaked runs:** check Nested `EM.run`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Ruby’s reactor for non-blocking network I/O — same idea as Node’s event loop: on…).
- **Con / when not:** **New Node services**
- **Con / when not:** **CPU-heavy workers**

## Comparison
- vs [[Event Loop]]: know when each applies


### Use cases
- In production APIs and tooling, **EventMachine** shows up whenever teams ship…
