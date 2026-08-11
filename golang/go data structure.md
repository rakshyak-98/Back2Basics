[[golang]] [[go features]] [[array]]

# go data structure

> Go builtins — arrays (fixed), slices (view+len+cap), maps (hash), structs (records); pick by growth and ownership.

---

## Mental model

**Say it in one breath:** Slice header = pointer+len+cap into an array. Append may reallocate. Maps are reference types; never assume range order. Structs group fields; copy is shallow.

```txt
slice:  ptr ──► [........] array
        len
        cap
```

| Type | When |
|------|------|
| Array `[N]T` | Fixed size known |
| Slice `[]T` | Growable sequences |
| Map `map[K]V` | Key lookup |
| Struct | Typed records |

---

## Standard config / commands

```go
s := make([]int, 0, 64)
s = append(s, 1, 2)
t := append([]int(nil), s...) // copy

m := map[string]int{"a": 1}
v, ok := m["a"]

type User struct {
  ID   string `json:"id"`
  Name string `json:"name"`
}
```

| Knob | Why it matters |
|------|----------------|
| `make([], 0, cap)` | Fewer allocs |
| `copy` / clone | Avoid alias bugs |
| Map key constraints | Comparable types only |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected shared mutation | Slice alias | Copy before mutate |
| Append overwrote other slice | Shared array | Full copy / force new cap |
| `assignment to entry in nil map` | Nil map | `make(map[…]…)` |
| Slow append in loop | Cap 0 growth | Preallocate |
| JSON empty vs null | Pointer fields | Use pointers / omitempty care |

---

## Gotchas

> [!WARNING]
> **Subslice shares backing array** — mutating one can change another.

> [!WARNING]
> **Nil vs empty slice** — both `len 0`; JSON encodes differently sometimes.

> [!WARNING]
> **Map not concurrency-safe** — mutex or `sync.Map` with eyes open.

---

## When NOT to use

- **Map as ordered list** — keep a slice of keys.
- **Giant arrays on stack** — heap/`make`.
- **Linked lists by default** — slices usually win in Go.

---

## Related

[[go features]] [[Unbuffered channel]] [[array]] [[Sorting algorithm]]
