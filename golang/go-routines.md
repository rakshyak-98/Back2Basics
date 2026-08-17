[[golang]] [[Unbuffered channel]] [[go error]] [[go debugging]] [[Thread]]

# go-routines

> Goroutine — lightweight concurrent function the Go runtime schedules onto OS threads (`go f()`).





## Interview Relevance
Goroutines + scheduler questions separate “cheap threads” myths from M:N scheduling, leaks, and when channels vs mutexes fit.

## Sources
- [Go blog — Concurrency is not parallelism](https://go.dev/blog/concurrency-is-not-parallelism) — overview
- [Go scheduler design notes (G-M-P)](https://go.dev/src/runtime/proc.go) — deep-dive
- [Effective Go — Concurrency](https://go.dev/doc/effective_go#concurrency) — deep-dive

## Key Concepts
```txt
main ──go worker()──► runnable queue ──► OS threads (GOMAXPROCS)
```

| Primitive | Role |
|-----------|------|
| Channel | Communicate / sync |
| `sync.Mutex` | Protect memory |
| `WaitGroup` | Wait for N exits |
| `context` | Cancel / deadline |

## Technical Details
```go
var wg sync.WaitGroup
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

wg.Add(1)
go func() {
  defer wg.Done()
  for {
    select {
    case <-ctx.Done():
      return
    case e := <-events:
      fmt.Println(e)
    }
  }
}()
wg.Wait()
```

| Knob | Why it matters |
|------|----------------|
| `GOMAXPROCS` | Parallel CPU threads |
| Exit condition | Avoid leaks |
| Don’t share without sync | Data races |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Leak (goroutine forever) | `runtime.NumGoroutine` / pprof | Cancel context; close chans |
| Data race | `go test -race` | Mutex or channel ownership |
| Panic kills process | Unrecovered panic in goroutine | Recover at boundary; log |
| Main exits early | No WaitGroup | Wait before return |
| Too many goroutines | Unbounded spawn | Worker pool |

## Pros/Cons or Trade-offs
- **Trade-off:** Tiny sync work — plain function call.
- **Trade-off:** One goroutine per request without limits — bound concurrency.
- **Trade-off:** Sharing structs “carefully” — prefer message passing or clear mutex.

## Mistakes to Avoid
- Loop variable capture (old Go) — pass `v := v` or use Go 1.22+ per-iter semantics.
- No join without sync — `go f()` alone doesn’t wait.
- Blocking forever on chan — always plan cancellation.
