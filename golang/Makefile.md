[[golang]] [[go cli]] [[go build]] [[go project]]

# Makefile

> Makefile for Go — thin wrapper around `go test`/`go build` so CI and humans share one entrypoint (this note is about Makefiles, not a real build file in the vault).

```txt
        Makefile ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you use Make as a thin, portable entrypoint over `…

## Sources
- [GNU Make manual](https://www.gnu.org/software/make/manual/make.html) — deep-dive
- [Go — How to Write Go Code](https://go.dev/doc/code) — overview

## Key Concepts
```txt
make test  → go test ./...
make build → go build -o bin/app ./cmd/app
```

| Target | Typical recipe |
|--------|----------------|
| `test` | `go test ./...` |
| `lint` | `golangci-lint run` |
| `build` | `go build …` |
| `run` | `go run ./cmd/app` |

## Technical Details
```makefile
.PHONY: test build run tidy

test:
	go test ./... -count=1

build:
	go build -trimpath -o bin/app ./cmd/app

tidy:
	go mod tidy

run: build
	./bin/app
```

| Knob | Why it matters |
|------|----------------|
| `.PHONY` | Always run non-file targets |
| Tabs | Recipes must use tabs |
| Vars `$(GO)` | Override toolchain |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `missing separator` | Spaces instead of tab | Retab recipes |
| Stale binary | File target vs PHONY | Mark PHONY or depend correctly |
| Works locally CI fails | Env / modules cache | Match `GOFLAGS`; cache modules |
| Recursive make hell | Nested projects | One module-aware Makefile |

## Mistakes to Avoid
- **Mistake:** Make doesn’t understand Go packages — always shell out to `go`
- **Mistake:** Silent `@` — hides commands; keep visible in CI
- **Mistake:** Windows

## Pros/Cons or Trade-offs
- **Trade-off:** Trivial one-package repository — raw `go test` is enough.
- **Trade-off:** Polyglot Bazel monorepo — use the monorepo tool.
- **Trade-off:** Replacing `go.mod` — never.
