[[golang]] [[go]] [[go package]] [[go functions]]

# go functions

> Functions — first-class values with multiple returns; methods are functions with a receiver.

## Mental model

**Say it in one breath:** `func` declares named or literal functions. Multiple results are normal (`(T, error)`). Methods hang off a type via receivers (value or pointer).

```txt
func Add(a, b int) int
func (s *Server) Start() error
f := func(x int) int { return x + 1 }
```

| Form | Use |
| --- | --- |
| Named | Package API |
| Method | Behavior on type |
| Closure | Capture env |
| Variadic `...T` | Soft argc |

## Standard config / commands

```go
func Load(path string) ([]byte, error) {
  b, err := os.ReadFile(path)
  if err != nil {
    return nil, fmt.Errorf("load %s: %w", path, err)
  }
  return b, nil
}

func (c *Client) Close() error { return c.conn.Close() }

sum := func(xs ...int) int {
  n := 0
  for _, x := range xs { n += x }
  return n
}
```

| Knob | Why it matters |

| Pointer receiver | Mutate / avoid big copies |
| --- | --- |
| Value receiver | Immutable small types |
| Named results | Rare; clarity vs opacity |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Method missing on interface | Value vs pointer receiver | Align method set |
| Closure sees final loop var | Captured loop var | Per-iter var (Go 1.22+) |
| Huge stack copies | Big struct value recv | Pointer receiver |
| Nil receiver panic | Called on nil | Guard or document |

## Gotchas

> [!WARNING]
> **No default args / overloads** — use options structs.

> [!WARNING]
> **Defer closes over vars** — watch loop + defer.

> [!WARNING]
> **First-class funcs aren’t generics substitutes** — use type params when needed.

## When NOT to use

- **God functions 200+ lines** — split.
- **Methods on every DTO** — keep domain focused.
- **Returning `any` everywhere** — type it.

## Related

[[go interface]] [[go error]] [[go package]] [[go-routines]]
