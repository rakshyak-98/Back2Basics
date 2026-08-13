[[golang]] [[go]] [[go package]] [[go debugging]]

# go cli

> `go` CLI — module, build, test, and dig into deps/memory with the standard toolchain.

---

## Index

- [[#Quick reference]]
- [[#Standard config / commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Standard config / commands

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

---

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

**Say it in one breath:** One binary drives modules (`mod`), compile (`build`/`run`), tests, and docs. Prefer `./...` patterns and modules over old `GOPATH` mode.

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Sum DB / checksum mismatch | Proxy / replace | `GOSUMDB`; fix replace |
| Stale cache weirdness | Bad build cache | `go clean -cache` |
| `unknown revision` | Tag missing | Pin commit / publish tag |
| Slow CI | Module download | Cache pkg mod; vendor if needed |
| Binary huge | Debug symbols | `-ldflags="-s -w"` |

---

## Gotchas

> [!WARNING]
> **`go get` on a main module** — prefer `go get pkg@version` explicitly.

> [!WARNING]
> **`pmap`/`/proc` are Linux ops tips** — not part of Go itself.

> [!WARNING]
> **`go run` rebuilds often** — use `build` for timing tests.

---

## When NOT to use

- **Non-Go monorepo orchestration** — Bazel/Make wrap `go`, don’t replace understanding.
- **Editing `go.sum` by hand** — never.
- **`GO111MODULE=off` in 2026** — modules only.

---

## Examples

```bash
# …
```

## Related

[[go]] [[Makefile]] [[go debugging]] [[go package]]
