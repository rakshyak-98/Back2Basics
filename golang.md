[[golang/go.md]] [[golang/go-routines]] [[golang/go interface]] [[golang/go error]] [[golang/go cli]] [[golang/go project]] [[INDEX]]

# golang

> Go — a compiled language built for simple concurrency and straightforward networked services; goroutines and interfaces dominate interviews.





## Interview Relevance
Go interviews probe goroutines/channels, interfaces (implicit satisfaction), error handling, and tooling (`go test`, modules, race detector). Signal: you know when *not* to over-channel.

## Sources
- [Go Language Specification](https://go.dev/ref/spec) — deep-dive
- [Effective Go](https://go.dev/doc/effective_go) — overview
- [Go Blog — Concurrency](https://go.dev/blog/pipelines) — deep-dive

## Core Definition
Go (Golang) is a statically typed, garbage-collected language with fast compile times, a single binary deployment model, and first-class concurrency via goroutines and channels.

## Key Concepts
- **Goroutines:** Lightweight concurrent functions ([[golang/go-routines]], [[golang/Unbuffered channel]]).
- **Interfaces:** Satisfied implicitly; small interfaces preferred ([[golang/go interface]]).
- **Errors:** Values, not exceptions; wrap with context ([[golang/go error]]).
- **Modules & packages:** Explicit dependency versions; package as API boundary ([[golang/go package]], [[golang/go project]]).
- **Tooling:** `go build`, `go test -race`, `go vet` ([[golang/go cli]], [[golang/go build]], [[golang/Makefile]]).

## Technical Details
```txt
go mod  →  packages  →  main
                │
                ├── goroutines + channels / contexts
                └── interfaces for test doubles
```

| Need | Note |
|------|------|
| Language tour | [[golang/go.md]] · [[golang/go learning]] |
| Concurrency | [[golang/go-routines]] · [[golang/Unbuffered channel]] |
| Design | [[golang/go SOLID]] · [[golang/go embedding]] |
| Debug | [[golang/go debugging]] · [[golang/go callstack]] |
| Data / strings | [[golang/go data structure]] · [[golang/go strings]] |

## Real-World Applications
API workers and CLIs that ship as one static-ish binary; sidecars and Kubernetes controllers; high-concurrency proxies where goroutine cost beats thread-per-connection models.

## Pros/Cons or Trade-offs
- **Pro:** Simple deployment; great standard library for HTTP/net; race detector.
- **Con:** Verbose errors; generics still maturing in codebases; easy to leak goroutines without `context` cancellation.

## Comparison
vs Node/Java: different concurrency story (goroutines vs event loop / threads). vs Rust: simpler memory model, less control. Sibling hub style: [[Docker]], [[Linux]] for the environments Go services run in.

## Mistakes to Avoid
- Unbounded goroutine spawn without backpressure.
- Sharing memory without sync or clear ownership (prefer communicating by channels *or* clear mutex rules — not neither).
- Ignoring `go test -race` in CI.
- Giant interfaces that mock poorly.
