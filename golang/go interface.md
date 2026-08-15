[[golang]] [[go]] [[go embedding]] [[go SOLID]] [[go functions]]

# go interface

> Interface — a method set; any type with those methods satisfies it **implicitly** (no `implements` keyword).

## Interview Relevance

Interfaces are Go’s polymorphism story — implicit satisfaction, small interfaces, and the empty interface/`any` trap.

## Sources

- [Go blog — The Laws of Reflection](https://go.dev/blog/laws-of-reflection) — deep-dive
- [Effective Go — Interfaces](https://go.dev/doc/effective_go#interfaces) — overview

## Key Concepts

```txt
package userapi
type Store interface { Get(id string) (User, error) }

package postgres // never imports userapi
func (s *Store) Get(id string) (User, error) { … }
```

| Idea | Practice |
|------|----------|
| Accept interfaces | Func params |
| Return concrete | Usually structs |
| Small interfaces | `io.Reader` style |

## Technical Details

```go
type Reader interface {
  Read(p []byte) (n int, err error)
}

var r Reader = bytes.NewReader([]byte("hi"))

// type assert
rc, ok := r.(io.ReadCloser)
```

| Knob | Why it matters |
|------|----------------|
| Pointer vs value receiver | Method set differs |
| Empty `interface{}` / `any` | Escape hatch |
| `errors.As` | Interface-ish probing |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Doesn’t satisfy interface | Pointer receiver missing | Use `*T` or change methods |
| Nil interface vs nil ptr | Typed nil stored | Return plain `nil` error |
| Fat interface hard to mock | Too many methods | Split interfaces |
| Import cycle | Interface next to concrete | Move interface to consumer |

## Pros/Cons or Trade-offs

- **Trade-off:** Single concrete forever — use the struct.
- **Trade-off:** “IUserService” with 30 methods — split or drop.
- **Trade-off:** Before writing tests — extract when mocking hurts.

## Mistakes to Avoid

- Interface holds (type, value) — nil concrete in non-nil interface ≠ nil.
- Don’t preemptively interface everything — wait for a second implementation / test need.
- Exported interface + unexported method — awkward; keep methods consistent.
