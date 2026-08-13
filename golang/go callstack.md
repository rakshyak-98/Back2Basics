[[golang]] [[go error]] [[go-routines]]

# go callstack

> Call stack unwind — Go walks frames backward on panic and runs each `defer` before the frame dies.

---

## How it works

```txt
panic
  ↓
for each frame (bottom → top):
  run defers (LIFO)
  pop frame
  ↓
crash  or  recover() at a defer boundary
```

| Piece | Job |
|-------|-----|
| Stack frame | One active call |
| `defer` | Cleanup on exit / panic |
| `recover` | Stop unwind inside a deferred func |

---


## Configuration and commands

```go
func safe() {
  defer func() {
    if r := recover(); r != nil {
      log.Printf("recovered: %v", r)
    }
  }()
  mayPanic()
}

// Print stack in logs
debug.PrintStack()
// or: panic value already includes stack in stderr
```

| Knob | Why it matters |
|------|----------------|
| `defer` placement | Runs even on early return |
| `recover` only in defer | Elsewhere always nil |
| Per-goroutine stack | Panic in one goroutine ≠ catch in another |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Process dies | Unrecovered panic | Recover at goroutine / HTTP boundary |
| Defers skipped? | Panic in other goroutine | Recover where panic runs |
| Huge stacks | Recursive panic / deep calls | Fix root; raise only if needed |
| Lost cleanup | No defer around resource | `defer f.Close()` |

---


## Gotchas

> [!WARNING]
> **`recover` outside defer is useless** — always returns nil.

> [!WARNING]
> **Sibling goroutine cannot recover your panic** — each stack is isolated.

---


## When not to use

- **Business errors** — return `error`, don’t panic + recover.
- **Cross-goroutine control flow** — use channels / context.

---


## Related

[[go error]] [[go-routines]] [[go debugging]] [[go functions]]

## Sources

- [Wikipedia — go callstack](https://en.wikipedia.org/wiki/go_callstack)
