[[golang]] [[go]] [[go project]] [[go cli]] [[go interface]] [[go functions]]

# go package

> Package — one directory of `.go` files compiled together; uppercase identifiers are exported across import boundaries.

```txt
        go package ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Package/visibility questions check uppercase export, one package per director…

## Sources
- [How to Write Go Code](https://go.dev/doc/code) — overview
- [Go spec — Packages](https://go.dev/ref/spec#Packages) — deep-dive

## Key Concepts
```txt
module github.com/acme/app
import "github.com/acme/app/internal/auth"
```

| Rule | Meaning |
|------|---------|
| One package / directory | Compilation unit |
| `Foo` vs `foo` | Exported vs private |
| `internal/` | Only parent tree may import |

## Technical Details
```bash
go list ./...
go doc encoding/json
go get golang.org/x/sync@latest
```

```go
package auth // directory auth/

func Public() {}  // exported
func private() {} // same package only
```

| Knob | Why it matters |
|------|----------------|
| `go.mod` module path | Base of all imports |
| `replace` | Local forks |
| `_` import | Side-effect init only |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `undefined: foo.Bar` | Unexported / wrong import | Capitalize or same package |
| Init cycle / import cycle | `go list -f '{{.ImportPath}}'` | Break cycle |
| Wrong package name | File mismatch in dir | Unify name |
| Stale deps | Old sum/mod | `go mod tidy` |

## Mistakes to Avoid
- **Mistake:** `init()` order — dependency order; keep `init` tiny
- **Mistake:** Test package `foo_test` — external test sees only exports
- **Mistake:** Blank import — only for registering drivers (`database/sql`)

## Pros/Cons or Trade-offs
- **Trade-off:** Micro-packages of one tiny function — prefer cohesive packages.
- **Trade-off:** Export everything “just in case” — keep API small.
- **Trade-off:** Circular “utils” bags — name by domain.
