[[golang/go embedding]] [[compiler/compiler]] [[Release cycle]] [[golang/go SOLID]] [[Docker/Docker compose]]

# go build

> `go build` compiles a module into a binary — modules replace GOPATH; cross-compile with `GOOS`/`GOARCH`.

```txt
        go build ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Build/module questions check modules vs GOPATH, cross-compile knobs (`GOOS`/`…

## Sources
- [Go — Modules reference](https://go.dev/ref/mod) — deep-dive
- [Go — Command go](https://pkg.go.dev/cmd/go) — deep-dive

## Key Concepts
```
go.mod (module path + require)
  → go build ./cmd/app
    → bin/app (static-ish binary)
```

## Technical Details
### Module init

```bash
go mod init github.com/org/app
go get github.com/lib/pq@v1.10.9
go mod tidy                    # add missing, drop unused
go mod verify
```

### Build patterns

```bash
go build -o bin/app ./cmd/app
go build -ldflags="-s -w" -trimpath ./...    # smaller prod binary
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app ./cmd/app
go install ./cmd/...           # puts binary in $GOBIN
```

### Useful flags

| Flag | Why |
|------|-----|
| `-race` | Data race detector (dev/test only) |
| `-tags prod` | Build tags for conditional files |
| `-ldflags "-X main.version=1.2.3"` | Inject version at link time |
| `-trimpath` | Reproducible builds (strip local paths) |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `cannot find module` | `go.mod` module path | `go mod init` correct path; private module GOPRIVATE |
| `checksum mismatch` | `go.sum` | `go mod tidy`; don't hand-edit sum |
| CGO errors on cross-compile | `CGO_ENABLED=1` | Disable CGO or cross toolchain |
| `main redeclared` | Multiple `main` packages | Build specific `./cmd/foo` path |
| Stale binary | Build cache | `go clean -cache` (last resort) |

## Mistakes to Avoid
- **Mistake:** Private modules
- **Mistake:** Working directory matters
- **Mistake:** for relative embed paths — use `//go:embed` from module root

## Pros/Cons or Trade-offs
- **Trade-off:** Don't commit `go.sum` deletes — always commit after `go mod tidy`.
- **Trade-off:** Don't vendor unless you have air-gap or reproducibility policy requiring it.
