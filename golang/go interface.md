[[golang]] [[go]] [[go embedding]]

# go interface

> Interface — a method set; any type with those methods satisfies it **implicitly** (no `implements` keyword).

## Mental model

**Say it in one breath:** Consumers define small interfaces for what they need; producers stay unaware. That inverts deps and avoids rigid `implements` graphs.

```txt
package userapi
type Store interface { Get(id string) (User, error) }

package postgres // never imports userapi
func (s *Store) Get(id string) (User, error) { … }
```

| Idea | Practice |
| --- | --- |
| Accept interfaces | Func params |
| Return concrete | Usually structs |
| Small interfaces | `io.Reader` style |

## Standard config / commands

```go
type Reader interface {
  Read(p []byte) (n int, err error)
}

var r Reader = bytes.NewReader([]byte("hi"))

// type assert
rc, ok := r.(io.ReadCloser)
```

| Knob | Why it matters |

| Pointer vs value receiver | Method set differs |
| --- | --- |
| Empty `interface{}` / `any` | Escape hatch |
| `errors.As` | Interface-ish probing |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Doesn’t satisfy interface | Pointer receiver missing | Use `*T` or change methods |
| Nil interface vs nil ptr | Typed nil stored | Return plain `nil` error |
| Fat interface hard to mock | Too many methods | Split interfaces |
| Import cycle | Interface next to concrete | Move interface to consumer |

## Gotchas

> [!WARNING]
> **Interface holds (type, value)** — nil concrete in non-nil interface ≠ nil.

> [!WARNING]
> **Don’t preemptively interface everything** — wait for a second implementation / test need.

> [!WARNING]
> **Exported interface + unexported method** — awkward; keep methods consistent.

## When NOT to use

- **Single concrete forever** — use the struct.
- **“IUserService” with 30 methods** — split or drop.
- **Before writing tests** — extract when mocking hurts.

## Related

[[go]] [[go embedding]] [[go SOLID]] [[go functions]]
