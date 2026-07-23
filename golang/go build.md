[[golang/go embedding]] [[compiler/compiler]] [[Release cycle]]

# go build

> Compile Go packages/binaries with module-aware dependency resolution — `go.mod` is the source of truth.

## Mental model

Go modules (`go.mod` + `go.sum`) replace GOPATH-era vendoring chaos. `go build` resolves imports, compiles packages, links a static binary (by default). Cross-compile via `GOOS`/`GOARCH`. Build cache lives in `$GOCACHE` — clean builds are rare after first compile.

```
go.mod (module path + require)
  → go build ./cmd/app
    → bin/app (static-ish binary)
```

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `cannot find module` | `go.mod` module path | `go mod init` correct path; private module GOPRIVATE |
| `checksum mismatch` | `go.sum` | `go mod tidy`; don't hand-edit sum |
| CGO errors on cross-compile | `CGO_ENABLED=1` | Disable CGO or cross toolchain |
| `main redeclared` | Multiple `main` packages | Build specific `./cmd/foo` path |
| Stale binary | Build cache | `go clean -cache` (last resort) |

## Gotchas

> [!WARNING]
> **Private modules** — set `GOPRIVATE=*.corp.com` and git credentials; CI needs same.
>
> **`-race` in prod** — 5–10× slower; never ship race binaries.
>
> **Working directory matters** for relative embed paths — use `//go:embed` from module root.

## When NOT to use

- Don't commit `go.sum` deletes — always commit after `go mod tidy`.
- Don't vendor unless you have air-gap or reproducibility policy requiring it.

## Related

[[golang/go SOLID]] [[golang/go embedding]] [[compiler/compiler]] [[Docker/Docker compose]]
