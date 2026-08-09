[[golang]] [[go package]] [[go project]]

# go

> Go — compiled language with packages, modules (`go.mod`), and `package main` + `func main` as the executable entry.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A **module** (`go.mod` path) versions a tree of **packages** (one directory = one package). `package main` builds a binary; other packages are libraries. Import paths are module-path + directory.

```txt
go.mod module path
   └── dir/package  ← import "module/dir"
package main → binary
```

| Idea | Go style |
|------|----------|
| Enums | `type Role string` + `const` |
| Inheritance | Embedding, not class trees |
| Visibility | Uppercase = exported |

---

## Standard config / commands

```bash
go mod init github.com/you/app
go get example.com/lib@v1.2.3
go mod tidy
go run ./cmd/app
go build -o bin/app ./cmd/app
go test ./...
```

```go
package main

import "fmt"

func main() { fmt.Println("hi") }
```

| Knob | Why it matters |
|------|----------------|
| Module path | Unique import identity |
| Same package per dir | Compiler unit |
| `internal/` | Import firewall |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `package main` expected | Wrong package in cmd | Fix declaration |
| Import cycle | A↔B | Extract shared package |
| `cannot find module` | Bad path / replace | `go mod tidy`; fix replace |
| Multiple packages in dir | Mixed names | Split dirs |
| Enum “invalid value” | No exhaustiveness | Validate at boundaries |

---

## Gotchas

> [!WARNING]
> **All files in a dir share one package name** (except `_test` external tests).

> [!WARNING]
> **Folder name ≠ package name required** — but matching reduces pain.

> [!WARNING]
> **No real enums** — consts don’t stop arbitrary values.

---

## When NOT to use

- **One-off scripts with heavy FFI to Python ML** — call out or use another runtime.
- **GUI-heavy desktop** — possible, not Go’s sweet spot.
- **Tiny glue without concurrency needs** — shell may be enough.

---

## Related

[[go package]] [[go cli]] [[go project]] [[go interface]]
