[[golang/go.md]] [[golang/go-routines]] [[golang/go interface]] [[golang/go error]] [[golang/go cli]] [[golang/go project]] [[INDEX]]

# golang

> Go — a compiled language built for simple concurrency and straightforward networked services; goroutines and interfaces dominate interviews.

```txt
        golang ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Go interviews probe goroutines/channels, interfaces (implicit satisfaction), …

## Sources
- [Go Language Specification](https://go.dev/ref/spec) — deep-dive
- [Effective Go](https://go.dev/doc/effective_go) — overview
- [Go Blog — Concurrency](https://go.dev/blog/pipelines) — deep-dive

## Key Concepts
- **Goroutines:** Lightweight concurrent functions ([[golang/go-routines]], [[golang/Unbuffered…
- **Interfaces:** Satisfied implicitly; small interfaces preferred ([[golang/go interface]]).
- **Errors:** Values, not exceptions; wrap with context ([[golang/go error]]).
- **Modules & packages:** Explicit dependency versions
- **Tooling:** `go build`, `go test -race`, `go vet` ([[golang/go cli]], [[golang/go build]]…


- **Core:** Go (Golang) is a statically typed, garbage-collected language with fast compi…

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

## Mistakes to Avoid
- **Mistake:** Unbounded goroutine spawn without backpressure
- **Mistake:** Sharing memory without sync or clear ownership (prefer communica…
- **Mistake:** Ignoring `go test -race` in CI
- **Mistake:** Giant interfaces that mock poorly

## Pros/Cons or Trade-offs
- **Pro:** Simple deployment; great standard library for HTTP/net; race detector.
- **Con:** Verbose errors; generics still maturing in codebases; easy to leak goroutines without `context` cancellation.

## Comparison
- vs Node/Java: different concurrency story (goroutines vs event loop / threads)


### Use cases
- API workers and CLIs that ship as one static-ish binary
