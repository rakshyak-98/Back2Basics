[[golang]] [[go]] [[go package]] [[go debugging]] [[Makefile]]

# go cli

> `go` CLI — module, build, test, and dig into deps/memory with the standard toolchain.

## Interview Relevance

The `go` tool is daily driver literacy — modules, test, vet, and profiling entrypoints signal you can operate a Go codebase without IDE magic.

## Sources

- [Go — Command go](https://pkg.go.dev/cmd/go) — deep-dive
- [Go — About the go command](https://go.dev/doc/go-commands) — overview

## Key Concepts

```txt
go mod init → edit code → go test ./... → go build
```

| Command | Job |
|---------|-----|
| `go mod tidy` | Sync require/sum |
| `go run` | Compile+run |
| `go build` / `install` | Artifact |
| `go test -race` | Race detector |
| `go doc` | Quick docs |

## Technical Details

```bash
go mod init github.com/you/app
go get example.com/lib@v1.2.3
go mod tidy && go mod verify
go run ./cmd/app
go build -trimpath -ldflags="-s -w" -o bin/app ./cmd/app
go test ./... -count=1
go test -race ./...
go list -m all
go clean -cache
go mod edit -replace example.com/lib=../lib
```

```bash
# memory snapshot while running
go run . & pid=$!; sleep 1; pmap -x $pid | head
grep Vm /proc/$pid/status
```

| Knob | Why it matters |
|------|----------------|
| `-race` | Catch data races |
| `-trimpath` | Reproducible builds |
| `replace` | Local module override |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Sum DB / checksum mismatch | Proxy / replace | `GOSUMDB`; fix replace |
| Stale cache weirdness | Bad build cache | `go clean -cache` |
| `unknown revision` | Tag missing | Pin commit / publish tag |
| Slow CI | Module download | Cache pkg mod; vendor if needed |
| Binary huge | Debug symbols | `-ldflags="-s -w"` |

### Quick reference

| Task | Command |
|------|---------|
| … | `…` |

### Options and flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Pros/Cons or Trade-offs

- **Trade-off:** Non-Go monorepo orchestration — Bazel/Make wrap `go`, don’t replace understanding.
- **Trade-off:** Editing `go.sum` by hand — never.
- **Trade-off:** `GO111MODULE=off` in 2026 — modules only.

## Mistakes to Avoid

- `go get` on a main module — prefer `go get pkg@version` explicitly.
- `pmap`/`/proc` are Linux ops tips — not part of Go itself.
- `go run` rebuilds often — use `build` for timing tests.
