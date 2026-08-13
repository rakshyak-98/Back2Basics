<!-- note-strategy: operational -->
[[golang]] [[go embedding]] [[go interface]]

# go features

> Go language shape — no class inheritance; embed structs, satisfy interfaces implicitly, maps iterate randomly on purpose.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Prefer composition. Embed a struct to promote its methods; shadow to override. Interfaces are satisfied by method sets — no `implements` keyword. Map range order is intentionally shuffled.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Method not promoted | Unexported / wrong embed | Export; embed by value/pointer correctly |
| Flaky map tests | Assumed order | Sort keys |
| “Doesn’t implement” | Pointer receiver only | Pass `*T` or add value method |
| Unexpected Eat() | Shadow vs promote | Call `c.Animal.Eat()` explicitly |

---

## Gotchas

> [!WARNING]
> **Embedding ≠ inheritance** — no polymorphic “base” type; use interfaces.

> [!WARNING]
> **Map iteration order** — never ship logic that depends on it.

---

## When NOT to use

- **Deep “is-a” trees** — redesign with interfaces + small structs.
- **Ordered maps as API** — use slices or sorted keys.

---

## Related

[[go embedding]] [[go interface]] [[go data structure]] [[go]]
