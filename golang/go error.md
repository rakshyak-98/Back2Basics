[[golang]] [[go callstack]] [[go-routines]]

# go error

> Go errors — values you return (`error` interface), not exceptions; `panic` is for truly unrecoverable surprises.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Normal failures are `return err`. Check with `if err != nil`. Wrap with `%w` for `errors.Is`/`As`. Nil pointer deref and friends become **panics** with a stack — fix the bug, don’t `recover` everywhere.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Nil pointer panic | Unchecked pointer / interface | Guard; init; read stack frame |
| Lost root cause | `%v` string wrap | Use `%w` |
| `err == ErrX` false | Wrapped | `errors.Is` |
| Panic in goroutine | No recover | Handle inside goroutine; log |
| Silent ignore | `_ = f()` | Never drop err in prod paths |

---

## Gotchas

> [!WARNING]
> **`(*T)(nil)` in interface is not nil error** — typed nil interface pitfall.

> [!WARNING]
> **Don’t panic for user input** — return `error`.

> [!WARNING]
> **Stack traces** — panics have them; plain `error` needs wrapping context.

---

## When NOT to use

- **Panic for control flow** — never.
- **`recover` in every function** — hides bugs.
- **Stringly errors only** — use types/sentinels for branches.

---

## Related

[[go callstack]] [[go-routines]] [[go debugging]] [[go functions]]
