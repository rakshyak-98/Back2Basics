[[golang]] [[go callstack]] [[go-routines]] [[go debugging]] [[go functions]]

# go error

> Go errors — values you return (`error` interface), not exceptions; `panic` is for truly unrecoverable surprises.

```txt
        go error ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Error handling is the Go culture check

## Sources
- [Go blog — Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors) — deep-dive
- [pkg.go.dev — errors](https://pkg.go.dev/errors) — deep-dive

## Key Concepts
```txt
f() (T, error)
   └─ caller checks err
panic ──unwinds──► defers run ──► crash (or recover)
```

| Tool | Job |
|------|-----|
| `error` | Expected failure |
| `fmt.Errorf("%w", err)` | Wrap preserve chain |
| `panic` / `recover` | Abort / boundary only |

## Technical Details
```go
if err != nil {
  return fmt.Errorf("load config: %w", err)
}

var pathErr *os.PathError
if errors.As(err, &pathErr) { /* … */ }
if errors.Is(err, fs.ErrNotExist) { /* … */ }

// nil deref looks like:
// panic: runtime error: invalid memory address or nil pointer dereference
```

| Knob | Why it matters |
|------|----------------|
| Sentinel errors | `var ErrX = errors.New(…)` |
| `%w` vs `%v` | Wrapping vs stringifying |
| `defer recover` | Only at goroutine / http boundaries |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Nil pointer panic | Unchecked pointer / interface | Guard; init; read stack frame |
| Lost root cause | `%v` string wrap | Use `%w` |
| `err == ErrX` false | Wrapped | `errors.Is` |
| Panic in goroutine | No recover | Handle inside goroutine; log |
| Silent ignore | `_ = f()` | Never drop err in prod paths |

## Mistakes to Avoid
- **Mistake:** **`(*T)(nil)` in interface is not nil error**
- **Mistake:** Don’t panic for user input — return `error`
- **Mistake:** Stack traces

## Pros/Cons or Trade-offs
- **Trade-off:** Panic for control flow — never.
- **Trade-off:** `recover` in every function — hides bugs.
- **Trade-off:** Stringly errors only — use types/sentinels for branches.
