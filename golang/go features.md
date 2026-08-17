[[golang]] [[go embedding]] [[go interface]] [[go data structure]] [[go]]

# go features

> Go language shape — no class inheritance; embed structs, satisfy interfaces implicitly, maps iterate randomly on purpose.

```txt
        go features ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Language-shape questions (no inheritance, implicit interfaces, random map ran…

## Sources
- [Effective Go](https://go.dev/doc/effective_go) — deep-dive
- [Go FAQ](https://go.dev/doc/faq) — overview

## Key Concepts
```txt
Cat { Animal }  →  Cat.Eat() may shadow Animal.Eat()
type Reader interface { Read([]byte) (int, error) }
any type with Read(…) satisfies Reader
```

| Feature | Plain meaning |
|---------|---------------|
| Embedding | Promote fields/methods |
| Implicit interface | Duck typing with compile checks |
| Random map range | Don’t rely on order |

## Technical Details
```go
type Animal struct{}
func (a *Animal) Eat() { fmt.Println("Eating") }

type Cat struct{ Animal }
func (c *Cat) Eat() { fmt.Println("Cat eating") } // shadow

func main() {
  Cat{}.Eat() // Cat eating
  for k := range map[string]int{"a": 1, "b": 2} {
    _ = k // order varies
  }
}
```

| Knob | Why it matters |
|------|----------------|
| Value vs pointer receiver | Method set differs |
| Embedded name collision | Inner field needs `c.Animal.X` |
| `sort` for maps | Collect keys, sort, then iterate |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Method not promoted | Unexported / wrong embed | Export; embed by value/pointer correctly |
| Flaky map tests | Assumed order | Sort keys |
| “Doesn’t implement” | Pointer receiver only | Pass `*T` or add value method |
| Unexpected Eat() | Shadow vs promote | Call `c.Animal.Eat()` explicitly |

## Mistakes to Avoid
- **Mistake:** Embedding ≠ inheritance
- **Mistake:** Map iteration order — never ship logic that depends on it

## Pros/Cons or Trade-offs
- **Trade-off:** Deep “is-a” trees — redesign with interfaces + small structs.
- **Trade-off:** Ordered maps as API — use slices or sorted keys.
