[[golang]] [[go features]] [[array]] [[Unbuffered channel]] [[Sorting algorithm]]

# go data structure

> Go builtins — arrays (fixed), slices (view+len+cap), maps (hash), structs (records); pick by growth and ownership.

## Interview Relevance

Slices vs arrays vs maps are classic Go interview landmines — backing arrays, `len`/`cap`, map iteration randomness, and accidental aliasing.

## Sources

- [Go blog — Go Slices: usage and internals](https://go.dev/blog/slices-intro) — deep-dive
- [Go spec — Map types](https://go.dev/ref/spec#Map_types) — deep-dive

## Key Concepts

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

## Technical Details

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected shared mutation | Slice alias | Copy before mutate |
| Append overwrote other slice | Shared array | Full copy / force new cap |
| `assignment to entry in nil map` | Nil map | `make(map[…]…)` |
| Slow append in loop | Cap 0 growth | Preallocate |
| JSON empty vs null | Pointer fields | Use pointers / omitempty care |

## Pros/Cons or Trade-offs

- **Trade-off:** Map as ordered list — keep a slice of keys.
- **Trade-off:** Giant arrays on stack — heap/`make`.
- **Trade-off:** Linked lists by default — slices usually win in Go.

## Mistakes to Avoid

- Subslice shares backing array — mutating one can change another.
- Nil vs empty slice — both `len 0`; JSON encodes differently sometimes.
- Map not concurrency-safe — mutex or `sync.Map` with eyes open.
