[[Operating System]] [[file descriptors]] [[discriptors]] [[system call]] [[process]]

# Handle

> A handle is an opaque token the operating system returns so user mode can reference a kernel object without exposing its memory address — Windows HANDLEs and Unix file descriptors play the same role with different APIs.

On **Windows**, `CreateFile`, `OpenProcess`, and `CreateThread` return **HANDLE** values validated by the kernel object manager. On **Unix**, integers ([[file descriptors]]) index per-process tables. Both support duplication, inheritance to child [[process]]es, and leak debugging.

## Comparison

| Platform | Token | Close API |
|----------|-------|-----------|
| Linux / POSIX | int fd | `close()` |
| Windows | HANDLE | `CloseHandle()` |

Security: handles carry access rights (Windows DACL; Unix file permissions + `/proc` visibility).

Cross-platform libraries (Rust `std::fs::File`, Go `os.File`) wrap the native handle type.

## Sources

- Microsoft Learn — [Handles and Objects](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects)
- Russinovich, *Windows Internals*
- Wikipedia: [Handle (computing)](https://en.wikipedia.org/wiki/Handle_(computing))
