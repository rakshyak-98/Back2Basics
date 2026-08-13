[[golang]] [[go cli]] [[go error]] [[go callstack]]

# go debugging

> Debug Go — race detector, Delve, pprof, and logging beats printf-only when concurrency bites.

---

## How it works

```txt
repro → go test -race → pprof/goroutine → dlv if needed
```

| Tool | Job |
|------|-----|
| `-race` | Data races |
| `pprof` | CPU/heap/goroutines |
| `dlv` | Breakpoints |
| `GODEBUG` | Runtime traces |

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Flaky concurrent test | `-race` | Fix shared state |
| Deadlock hang | goroutine pprof | Missing unlock / chan peer |
| Memory climb | heap pprof | Find retainers |
| Can’t hit breakpoint | Optimized build | `gcflags` all=-N -l |
| Works in test not prod | Env / GOMAXPROCS | Match configs |

---


## Gotchas

> [!WARNING]
> **Race detector slows runs** — CI sample + local on concurrent pkgs.

> [!WARNING]
> **pprof without auth on public IP** — don’t.

> [!WARNING]
> **Optimizations hide vars in dlv** — disable for debug builds.

---


## When not to use

- **Printf forever** — fine for tiny scripts; not for races.
- **Production `dlv attach` casually** — prefer metrics/pprof first.
- **Ignoring failures that “retry works”** — usually a race.

---


## Related

[[go cli]] [[go-routines]] [[go callstack]] [[go error]]

## Sources

- [Wikipedia — go debugging](https://en.wikipedia.org/wiki/go_debugging)
