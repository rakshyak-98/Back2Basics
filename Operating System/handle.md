[[Operating System]] [[file descriptors]] [[discriptors]] [[system call]] [[process]]

# Handle

> A handle is an opaque token the OS returns so user mode can reference a kernel object without exposing its address — Windows HANDLEs and Unix file descriptors play the same role.

```txt
        Handle ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Cross-platform systems: opaque capability tokens, duplication/inheritance, an…

## Sources
- [Microsoft Learn — Handles and Objects](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects) — deep-dive
- Russinovich, *Windows Internals* — deep-dive
- [Wikipedia — Handle (computing)](https://en.wikipedia.org/wiki/Handle_(computing)) — overview

## Key Concepts
- **Opaque token:** not a raw pointer to kernel memory.
- **Unix form:** small int [[file descriptors]].
- **Windows form:** `HANDLE` from object manager APIs.
- **Lifecycle:** duplicate, inherit to child [[process]]es, close explicitly.

## Technical Details
| Platform | Token | Close API |
|----------|-------|-----------|
| Linux / POSIX | int fd | `close()` |
| Windows | HANDLE | `CloseHandle()` |

- Security: handles carry access rights (Windows DACL
- Cross-platform libs (`std::fs::File`, `os.File`) wrap the native type.

## Mistakes to Avoid
- **Mistake:** Double-close / use-after-close
- **Mistake:** Assuming a numeric HANDLE/fd value is meaningful across processe…
- **Mistake:** Leaking handles until process handle-table limits hit

## Pros/Cons or Trade-offs
- **Pro:** Safe indirection; kernel can revoke/validate.
- **Con:** Leaks; type confusion if casts are abused.
- **Trade-off:** richer Windows handle rights vs simpler Unix fd model.

## Comparison
- vs [[file descriptors]]: Unix specialization of the handle idea.
- vs raw pointers: handles survive kernel object moves/revocation better.


### Use cases
- Win32 services, Wine compatibility layers, and portable runtimes abstracting …
