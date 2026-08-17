[[golang]] [[go]] [[go package]] [[go functions]] [[go interface]] [[go error]] [[go-routines]]

# go functions

> Functions — first-class values with multiple returns; methods are functions with a receiver.





## Interview Relevance
Multiple returns, defer, and method receivers show up constantly — value vs pointer receiver and first-class functions are the depth checks.

## Sources
- [Go spec — Function types](https://go.dev/ref/spec#Function_types) — deep-dive
- [Effective Go — Functions](https://go.dev/doc/effective_go#functions) — overview

## Key Concepts
```txt
func Add(a, b int) int
func (s *Server) Start() error
f := func(x int) int { return x + 1 }
```

| Form | Use |
|------|-----|
| Named | Package API |
| Method | Behavior on type |
| Closure | Capture env |
| Variadic `...T` | Soft argc |

## Technical Details
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
|------|----------------|
| Pointer receiver | Mutate / avoid big copies |
| Value receiver | Immutable small types |
| Named results | Rare; clarity vs opacity |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Method missing on interface | Value vs pointer receiver | Align method set |
| Closure sees final loop var | Captured loop var | Per-iter var (Go 1.22+) |
| Huge stack copies | Big struct value recv | Pointer receiver |
| Nil receiver panic | Called on nil | Guard or document |

## Pros/Cons or Trade-offs
- **Trade-off:** God functions 200+ lines — split.
- **Trade-off:** Methods on every DTO — keep domain focused.
- **Trade-off:** Returning `any` everywhere — type it.

## Mistakes to Avoid
- No default args / overloads — use options structs.
- Defer closes over vars — watch loop + defer.
- First-class funcs aren’t generics substitutes — use type params when needed.
