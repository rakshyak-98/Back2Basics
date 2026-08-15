[[golang]] [[go-routines]] [[go error]] [[go debugging]]

# Unbuffered channel

> Unbuffered channel — send and receive happen together; no queue — the handoff *is* the sync point.

## Interview Relevance

Channels are a Go concurrency staple in interviews — they want rendezvous vs buffer, close ownership, and deadlock/leak reasoning, not just `go` keyword trivia.

## Sources

- [Go blog — Share Memory By Communicating](https://go.dev/blog/codelab-share) — overview
- [Go spec — Channel types](https://go.dev/ref/spec#Channel_types) — deep-dive

## Key Concepts

```txt
goroutine A: ch <- v   ──rendezvous──►  goroutine B: <-ch
```

| Kind | Behavior |
|------|----------|
| Unbuffered | Sync handoff |
| Buffered `make(chan T, n)` | Queue up to `n`, then block |

## Technical Details

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Deadlock all goroutines asleep | Send with no recv (or opposite) | Ensure peer; use buffered sparingly |
| Leak goroutine | Blocked on chan forever | Context cancel; close carefully |
| Panic send on closed | Closed too early | Close once from sender |
| Race on close | Multiple closers | `sync.Once` or one owner |

## Pros/Cons or Trade-offs

- **Trade-off:** Need burst decoupling — use buffered or a queue.
- **Trade-off:** Fan-out CPU work — worker pool with bounded buffer.
- **Trade-off:** Simple mutex-protected state — sometimes a mutex is clearer.

## Mistakes to Avoid

- Nil channel blocks forever — `var ch chan int`; send/recv hang.
- Don’t close from receiver — ownership rule: sender closes.
- Range exits only on close — forgetting close = forever loop.
