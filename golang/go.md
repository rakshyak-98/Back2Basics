[[golang]] [[go package]] [[go project]] [[go cli]] [[go interface]]

# go

> Go — compiled language with packages, modules (`go.mod`), and `package main` + `func main` as the executable entry.

```txt
        go ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers expect the Go mental model: compiled packages/modules, `package …

## Sources
- [Go documentation](https://go.dev/doc/) — overview
- [Go spec](https://go.dev/ref/spec) — deep-dive

## Key Concepts
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

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `package main` expected | Wrong package in cmd | Fix declaration |
| Import cycle | A↔B | Extract shared package |
| `cannot find module` | Bad path / replace | `go mod tidy`; fix replace |
| Multiple packages in dir | Mixed names | Split dirs |
| Enum “invalid value” | No exhaustiveness | Validate at boundaries |

## Mistakes to Avoid
- **Mistake:** **All files in a dir share one package name** (except `_test` ex…
- **Mistake:** Folder name ≠ package name required — but matching reduces pain
- **Mistake:** No real enums — consts don’t stop arbitrary values

## Pros/Cons or Trade-offs
- **Trade-off:** One-off scripts with heavy FFI to Python ML — call out or use another runtime.
- **Trade-off:** GUI-heavy desktop — possible, not Go’s sweet spot.
- **Trade-off:** Tiny glue without concurrency needs — shell may be enough.
