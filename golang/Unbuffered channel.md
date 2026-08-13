[[golang]] [[go-routines]]

# Unbuffered channel

> Unbuffered channel — send and receive happen together; no queue — the handoff *is* the sync point.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `make(chan T)` has capacity 0. Sender blocks until a receiver is ready (and vice versa). Guarantees happens-before between the two sides.

```txt
goroutine A: ch <- v   ──rendezvous──►  goroutine B: <-ch
```

| Kind | Behavior |
|------|----------|
| Unbuffered | Sync handoff |
| Buffered `make(chan T, n)` | Queue up to `n`, then block |

---

## Standard config / commands

```go
ch := make(chan int) // unbuffered

go func() { ch <- 42 }()
v := <-ch

// close only from sender side when done
close(ch)
for v := range ch { /* … */ }
```

| Knob | Why it matters |
|------|----------------|
| Capacity 0 vs `n` | Coupling vs decoupling |
| Close | Receivers see zero value + `ok=false` |
| Select | Multi-channel / timeout |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Deadlock all goroutines asleep | Send with no recv (or opposite) | Ensure peer; use buffered sparingly |
| Leak goroutine | Blocked on chan forever | Context cancel; close carefully |
| Panic send on closed | Closed too early | Close once from sender |
| Race on close | Multiple closers | `sync.Once` or one owner |

---

## Gotchas

> [!WARNING]
> **Nil channel blocks forever** — `var ch chan int`; send/recv hang.

> [!WARNING]
> **Don’t close from receiver** — ownership rule: sender closes.

> [!WARNING]
> **Range exits only on close** — forgetting close = forever loop.

---

## When NOT to use

- **Need burst decoupling** — use buffered or a queue.
- **Fan-out CPU work** — worker pool with bounded buffer.
- **Simple mutex-protected state** — sometimes a mutex is clearer.

---

## Related

[[go-routines]] [[go error]] [[go debugging]]
