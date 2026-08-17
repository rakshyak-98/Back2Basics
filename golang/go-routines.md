[[golang]] [[Unbuffered channel]] [[go error]] [[go debugging]] [[Thread]]

# go-routines

> Goroutine — lightweight concurrent function the Go runtime schedules onto OS threads (`go f()`).

```txt
        go-routines ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Goroutines + scheduler questions separate “cheap threads” myths from M:N sche…

## Sources
- [Go blog — Concurrency is not parallelism](https://go.dev/blog/concurrency-is-not-parallelism) — overview
- [Go scheduler design notes (G-M-P)](https://go.dev/src/runtime/proc.go) — deep-dive
- [Effective Go — Concurrency](https://go.dev/doc/effective_go#concurrency) — deep-dive

## Key Concepts
```txt
- **Note:** main ──go worker()──► runnable queue ──► OS threads (GOMAXPROCS)
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

## Mistakes to Avoid
- **Mistake:** Loop variable capture (old Go)
- **Mistake:** No join without sync — `go f()` alone doesn’t wait
- **Mistake:** Blocking forever on chan — always plan cancellation

## Pros/Cons or Trade-offs
- **Trade-off:** Tiny sync work — plain function call.
- **Trade-off:** One goroutine per request without limits — bound concurrency.
- **Trade-off:** Sharing structs “carefully” — prefer message passing or clear mutex.
