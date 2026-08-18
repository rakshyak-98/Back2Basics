[[golang]] [[Unbuffered channel]] [[go error]]

# go-routines

> Goroutine — lightweight concurrent function the Go runtime schedules onto OS threads (`go f()`).

## Mental model

**Say it in one breath:** `go` starts work that can run interleaved with other goroutines. Cheap stacks (~KB), multiplexed by the runtime. You still need sync: channels, mutexes, `WaitGroup`, `context`.

```txt
main ──go worker()──► runnable queue ──► OS threads (GOMAXPROCS)
```

| Primitive | Role |
| --- | --- |
| Channel | Communicate / sync |
| `sync.Mutex` | Protect memory |
| `WaitGroup` | Wait for N exits |
| `context` | Cancel / deadline |

## Standard config / commands

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

| `GOMAXPROCS` | Parallel CPU threads |
| --- | --- |
| Exit condition | Avoid leaks |
| Don’t share without sync | Data races |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Leak (goroutine forever) | `runtime.NumGoroutine` / pprof | Cancel context; close chans |
| Data race | `go test -race` | Mutex or channel ownership |
| Panic kills process | Unrecovered panic in goroutine | Recover at boundary; log |
| Main exits early | No WaitGroup | Wait before return |
| Too many goroutines | Unbounded spawn | Worker pool |

## Gotchas

> [!WARNING]
> **Loop variable capture (old Go)** — pass `v := v` or use Go 1.22+ per-iter semantics.

> [!WARNING]
> **No join without sync** — `go f()` alone doesn’t wait.

> [!WARNING]
> **Blocking forever on chan** — always plan cancellation.

## When NOT to use

- **Tiny sync work** — plain function call.
- **One goroutine per request without limits** — bound concurrency.
- **Sharing structs “carefully”** — prefer message passing or clear mutex.

## Related

[[Unbuffered channel]] [[go error]] [[go debugging]] [[Thread]]
