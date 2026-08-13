<!-- note-strategy: operational -->
[[golang]] [[go]] [[go project]]

# go package

> Package — one directory of `.go` files compiled together; uppercase identifiers are exported across import boundaries.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `package foo` at the top of every file in `…/foo`. Importers use the module path + folder. Modules (`go.mod`) version a set of packages.

```txt
module github.com/acme/app
import "github.com/acme/app/internal/auth"
```

| Rule | Meaning |
|------|---------|
| One package / directory | Compilation unit |
| `Foo` vs `foo` | Exported vs private |
| `internal/` | Only parent tree may import |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `undefined: foo.Bar` | Unexported / wrong import | Capitalize or same package |
| Init cycle / import cycle | `go list -f '{{.ImportPath}}'` | Break cycle |
| Wrong package name | File mismatch in dir | Unify name |
| Stale deps | Old sum/mod | `go mod tidy` |

---

## Gotchas

> [!WARNING]
> **`init()` order** — dependency order; keep `init` tiny.

> [!WARNING]
> **Test package `foo_test`** — external test sees only exports.

> [!WARNING]
> **Blank import** — only for registering drivers (`database/sql`).

---

## When NOT to use

- **Micro-packages of one tiny function** — prefer cohesive packages.
- **Export everything “just in case”** — keep API small.
- **Circular “utils” bags** — name by domain.

---

## Related

[[go]] [[go cli]] [[go interface]] [[go functions]]
