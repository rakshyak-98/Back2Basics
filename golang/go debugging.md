[[golang]] [[go cli]] [[go error]] [[go callstack]] [[go-routines]]

# go debugging

> Debug Go — race detector, Delve, pprof, and logging beats printf-only when concurrency bites.

```txt
        go debugging ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Debugging questions check race detector, Delve, and pprof

## Sources
- [Go blog — Introducing the Go Race Detector](https://go.dev/blog/race-detector) — overview
- [Diagnostics — Profiling](https://go.dev/doc/diagnostics) — deep-dive
- [Delve docs](https://github.com/go-delve/delve/tree/master/Documentation) — deep-dive

## Key Concepts
```txt
repro → go test -race → pprof/goroutine → dlv if needed
```

| Tool | Job |
|------|-----|
| `-race` | Data races |
| `pprof` | CPU/heap/goroutines |
| `dlv` | Breakpoints |
| `GODEBUG` | Runtime traces |

## Technical Details
```bash
go test -race ./...
go test -run TestFoo -v -count=1

go test -cpuprofile=cpu.out ./pkg
go tool pprof cpu.out

import _ "net/http/pprof"
# then: go tool pprof http://localhost:6060/debug/pprof/profile

dlv test ./pkg -- -test.run TestFoo
dlv exec ./bin/app
```

| Knob | Why it matters |
|------|----------------|
| `-count=1` | Disable test cache |
| `GOTRACEBACK=all` | Fuller panic stacks |
| `http/pprof` | Prod-safe only behind auth |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Flaky concurrent test | `-race` | Fix shared state |
| Deadlock hang | goroutine pprof | Missing unlock / chan peer |
| Memory climb | heap pprof | Find retainers |
| Can’t hit breakpoint | Optimized build | `gcflags` all=-N -l |
| Works in test not prod | Env / GOMAXPROCS | Match configs |

## Mistakes to Avoid
- **Mistake:** Race detector slows runs — CI sample + local on concurrent pkgs
- **Mistake:** pprof without auth on public IP — don’t
- **Mistake:** Optimizations hide vars in dlv — disable for debug builds

## Pros/Cons or Trade-offs
- **Trade-off:** Printf forever — fine for tiny scripts; not for races.
- **Trade-off:** Production `dlv attach` casually — prefer metrics/pprof first.
- **Trade-off:** Ignoring failures that “retry works” — usually a race.
