[[golang]] [[go cli]] [[go build]]

# Makefile

> Makefile for Go — thin wrapper around `go test`/`go build` so CI and humans share one entrypoint (this note is about Makefiles, not a real build file in the vault).

---

## Mental model

**Say it in one breath:** Make lists targets with recipes. For Go, targets usually call the Go toolchain — don’t reimplement module logic in Make.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `missing separator` | Spaces instead of tab | Retab recipes |
| Stale binary | File target vs PHONY | Mark PHONY or depend correctly |
| Works locally CI fails | Env / modules cache | Match `GOFLAGS`; cache modules |
| Recursive make hell | Nested projects | One module-aware Makefile |

---

## Gotchas

> [!WARNING]
> **Make doesn’t understand Go packages** — always shell out to `go`.

> [!WARNING]
> **Silent `@`** — hides commands; keep visible in CI.

> [!WARNING]
> **Windows** — prefer `task`/`just` or scripts if team isn’t Make-fluent.

---

## When NOT to use

- **Trivial one-package repo** — raw `go test` is enough.
- **Polyglot Bazel monorepo** — use the monorepo tool.
- **Replacing `go.mod`** — never.

---

## Related

[[go cli]] [[go build]] [[go project]]
