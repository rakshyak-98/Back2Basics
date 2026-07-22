[[file descriptors]] [[fsync]] [[Buffer cache]] [[mmap]] [[multiple levels of buffering]]

# How to manipulate memory directly

> Direct memory access patterns — `mmap`, pointers, unsafe escape hatches — and when **not** to touch raw memory — **Stevens / Rustonomicon / Go unsafe rules**.

---

## Mental model

Normal code uses **managed abstractions**: language runtime, GC, copy-on-write pages. **Direct memory** means you hold a raw address into process virtual memory — reading/writing bytes with no bounds checker, or mapping file bytes into your address space without `read()` copies.

```txt
read()/write() path:  kernel page cache ──copy──► userspace buffer
mmap() path:          userspace pointer ──► same page cache pages (shared mapping)
```

| Mechanism | Language | Use case |
|-----------|----------|----------|
| **mmap(2)** | C, Rust, Go | Large files, zero-copy read, shared memory |
| **Pointers** | C, C++ | Embedded, kernels, hot loops |
| **`unsafe` Rust** | Rust | FFI, lock-free structures after proof |
| **`unsafe.Pointer` Go** | Go | syscall, cgo, `[]byte` ↔ struct overlay |
| **Direct ByteBuffer** | Java | NIO off-heap, Netty |

**Virtual memory** hides physical RAM; your pointer is a **virtual address**. Use-after-free, buffer overrun, and data races become security bugs — not test failures.

---

## Standard config / commands

### mmap — file-backed read (C)

```c
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

int fd = open("data.bin", O_RDONLY);
off_t len = lseek(fd, 0, SEEK_END);
void *p = mmap(NULL, len, PROT_READ, MAP_PRIVATE, fd, 0);
// read via ((char*)p)[i] — page fault loads from disk/cache
munmap(p, len);
close(fd);
```

`MAP_PRIVATE` + write → **copy-on-write** private page. `MAP_SHARED` + write → visible to other mappers; needs [[fsync]]/`msync` for durability to disk.

### Rust — safe wrapper pattern

```rust
use memmap2::MmapOptions;
use std::fs::File;

let file = File::open("data.bin")?;
let mmap = unsafe { MmapOptions::new().map(&file)? };
// &mmap[0..8] — bounds checked slice view
```

Keep `unsafe` block minimal; invariants documented.

### Go — slice from mmap (via syscall or x/sys/unix)

```go
// Prefer os.ReadFile for small files; mmap when file >> RAM or hot random access
data, _ := os.ReadFile("config.json") // copies — usually fine

// unsafe: string ↔ []byte zero-copy (Go 1.20+ has safer patterns)
// NEVER if bytes mutate while string live
```

Go rule: **avoid unsafe** unless cgo/syscall; `encoding/binary` + slices cover 99%.

### Link to [[file descriptors]] and buffers

```txt
fd open → read fills userspace []byte  (extra copy)
fd open → mmap maps page cache pages   (no copy on read)
write() → userspace → kernel buffer → disk (see [[multiple levels of buffering]])
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| SIGSEGV / segfault | core dump `gdb bt`; ASan | OOB pointer; use-after-free |
| Corrupt data after crash | `msync(MS_SYNC)` before unmap? | Durability: [[fsync]] file or `msync` shared mapping |
| Stale reads of live file | mmap without `MAP_SHARED` invalidation | Remap on change; or don't mmap mutating files |
| Heisenbug under load | ThreadSanitizer / `-race` | Data race on shared mmap region |
| Go GC issues with unsafe | `runtime.KeepAlive` | Premature collection of backing array |
| `Bus error` | Unaligned access on mapped device memory | Align or use `memcpy` |

```shell
# Debug mmap mappings
cat /proc/PID/maps | grep yourfile
valgrind --tool=memcheck ./app
```

---

## Gotchas

> [!WARNING]
> **String zero-copy in Go/Rust** — if underlying bytes mutate, string/hash invariant breaks silently.

> [!WARNING]
> **mmap + file truncate** — shrinking file while mapped → SIGBUS on access past new EOF.

> [!WARNING]
> **Huge pages / THP** — large mmap may trigger latency spikes on first touch; tune for latency-sensitive services.

> [!WARNING]
> **32-bit address space** — mapping multi-GB files fails; use chunked read or 64-bit process.

> [!WARNING]
> **Security** — parsing untrusted binary with pointer casts = remote exploit. Use validated parsers.

---

## When NOT to use

- **Default application code** — `read`, `WriteFile`, ORM, serde — correct and safe.
- **Network I/O** — use sockets/streams; don't mmap sockets.
- **"Performance" without profiling** — copy cost rarely dominates vs JSON parse/DB query.
- **Cross-language ownership** — raw pointers across FFI without documented lifetime = outage.

---

## Related

[[file descriptors]] [[fsync]] [[Buffer cache]] [[multiple levels of buffering]] [[mmap]] [[non-blocking]]
