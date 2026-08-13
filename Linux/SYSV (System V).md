<!-- note-strategy: operational -->
[[Linux]] [[ELF (Editabl Linkable File)]] [[linker]] [[stack pointer]] [[LSB (Linux Standard Base)]]

# SYSV (System V)

> System V ABI is the binary calling contract Linux uses on a given arch — how args, stack, and registers work so binaries and libs match.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Compilers, linkers, and the dynamic loader agree on register use, stack alignment, and symbol rules — that agreement is the ABI; on Linux ELF it’s usually labeled “UNIX - System V.”

```txt
Your .o / .so / executable
        │
        ├─ calling convention (args in regs / stack)
        ├─ stack layout & alignment
        ├─ syscall / PIC / TLS conventions
        └─ dynamic linker (ld.so) expectations
                 │
                 ▼
        runs only if ABI matches the system
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ABI** | Application Binary Interface | “Binary contract — not the C API source level.” |
| **System V ABI** | Common Unix/Linux ELF conventions | “`readelf` shows OS/ABI: UNIX - System V.” |
| **Calling convention** | Where args and return values live | “On amd64 SysV: rdi, rsi, rdx, … for args.” |
| **ELF** | Binary file format | “ABI lives inside ELF metadata and codegen.” |
| **ld.so** | Dynamic linker/loader | “Loads deps; wrong ABI → won’t start.” |
| **SysVinit (legacy)** | Old init system | “Different ‘SysV’ — boot scripts, not ABI.” |

> [!INFO]
> **Two “System V” meanings:** (1) **ABI / ELF** — what this note is about; (2) **SysVinit** — historic init (`/etc/init.d`). Don’t mix them in an interview.

### How the story goes (4 steps)

1. **Compile** — compiler emits code for a target ABI (e.g. SysV AMD64).
2. **Link** — objects agree on relocations and symbol sizes.
3. **Load** — `ld.so` maps segments and binds symbols.
4. **Call** — function calls obey the register/stack rules end-to-end.

---

## Standard config / commands

```bash
readelf -h ./binary | egrep 'Class|ELF Header|OS/ABI|Machine|Type'
# OS/ABI: UNIX - System V

readelf -d ./binary | grep NEEDED    # shared libs
file ./binary
objdump -f ./binary

# Cross-check arch
uname -m
readelf -A ./binary | head
```

| Knob | Why it matters |
|------|----------------|
| `-m64` / target triple | Wrong arch ABI → `Exec format error` |
| Static vs dynamic | Static embeds libc; still CPU ABI-bound |
| `DT_NEEDED` | Missing soname → loader errors |
| Softfloat vs hardfloat (ARM) | Classic ABI mismatch on embedded |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Exec format error` | `file` arch vs host | Right binary for arch |
| `error while loading shared libraries` | `ldd` / `LD_LIBRARY_PATH` | Install matching libs |
| Crash at first call into `.so` | ABI/calling mismatch | Rebuild both sides same toolchain flags |
| `OS/ABI` weird in readelf | Cross/odd toolchain | Expect SysV on Linux x86_64 |
| Old SysVinit scripts on systemd host | Distro uses systemd | Use [[systemd]] / [[systemctl]] |

---

## Gotchas

> [!WARNING]
> **API ≠ ABI.** Same C headers can still break if struct layout or calling convention differs.

> [!WARNING]
> **SysV AMD64 red zone** — 128 bytes below RSP scratch for leaf functions; interrupts must respect it in kernel paths; user bugs usually elsewhere.

> [!WARNING]
> **Mixing MSVC and SysV objects** on Windows/Linux ports — different ABIs; don’t link them raw.

> [!WARNING]
> **“System V IPC”** (sem/shm/msg) is yet another SysV phrase — see `ipcs`, not this ABI note.

---

## When NOT to use

- **Explaining source-level APIs** — talk POSIX/C standards, not SysV ABI.
- **Service management today** — prefer [[systemd]]; SysVinit is legacy on most distros.
- **Web/JSON services** — ABI concerns stop at the process boundary.

---

## Related

[[ELF (Editabl Linkable File)]] [[linker]] [[stack pointer]] [[LSB (Linux Standard Base)]] [[assembly language]] [[systemd]] [[opcode]]
