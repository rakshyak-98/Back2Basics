[[golang]] [[go error]] [[go-routines]] [[go debugging]] [[go functions]]

# go callstack

> Call stack unwind — Go walks frames backward on panic and runs each `defer` before the frame dies.

```txt
        go callstack ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Panic/defer unwind questions separate “errors as values” from stack unwinding

## Sources
- [Go spec — Defer statements](https://go.dev/ref/spec#Defer_statements) — deep-dive
- [Go blog — Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover) — overview

## Key Concepts
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

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Process dies | Unrecovered panic | Recover at goroutine / HTTP boundary |
| Defers skipped? | Panic in other goroutine | Recover where panic runs |
| Huge stacks | Recursive panic / deep calls | Fix root; raise only if needed |
| Lost cleanup | No defer around resource | `defer f.Close()` |

## Mistakes to Avoid
- **Mistake:** `recover` outside defer is useless — always returns nil
- **Mistake:** Sibling goroutine cannot recover your panic

## Pros/Cons or Trade-offs
- **Trade-off:** Business errors — return `error`, don’t panic + recover.
- **Trade-off:** Cross-goroutine control flow — use channels / context.
