[[Operating System/base clock speed]] [[Operating System/Single Instruction, Multiple Data (SIMD)]] [[Operating System/context switching]] [[AWS/AWS EC2]]

# Advanced RISC Machine (ARM)

> ARM (Advanced RISC Machine) — RISC load/store CPUs; AArch64 is the modern 64-bit server and mobile baseline.

```txt
        Advanced RISC Mach ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** ARM/AArch64 questions check RISC load/store thinking, calling conventions, an…

## Sources
- [Arm Architecture Reference Manual](https://developer.arm.com/documentation) — deep-dive
- [Wikipedia — ARM architecture family](https://en.wikipedia.org/wiki/ARM_architecture_family) — overview

## Key Concepts
- **Note:** **ARM** (Advanced RISC Machine) uses **Reduced Instruction Set Computing**: s…

```
- **Note:** Program Counter (PC) → fetch instruction → decode → execute → writeback
                              │
- **Note:** ARM pipeline: PC may read as current + offset (+8 bytes in AArch64 EL0 debug)
```

| vs x86 | ARM tendency |
|--------|--------------|
| Instruction density | Fixed 32-bit (A64); compact Thumb history on 32-bit ARM |
| Power | Better perf/W — Apple Silicon, Graviton |
| Ecosystem | Mobile first; Linux server growth (AWS Graviton) |

- **Note:** **PC quirk:** When reading PC in debug/asm, value often **points ahead** of c…

## Technical Details
### Check architecture (Linux)

```bash
uname -m          # aarch64 vs x86_64
lscpu | egrep 'Architecture|Model name|Flags'
cat /proc/cpuinfo | head
```

### Build for ARM (cross-compile Go)

```bash
GOOS=linux GOARCH=arm64 go build -o app-arm64 .
```

### Docker multi-arch

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### AWS Graviton (cost/perf)

- Choose `m7g` / `c7g` instance families — verify binary has **arm64** build
- Same application, ~20–40% better price-performance for many workloads versus …

### Debug register / PC (gdb)

```bash
gdb ./binary
(gdb) break main
(gdb) run
(gdb) info registers pc
# Compare with disassembly — expect offset from source line
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `Exec format error` | Wrong arch binary | Rebuild arm64 or use qemu-user |
| Illegal instruction | CPU feature mismatch | Check `-march`; avoid AVX-only code paths |
| Slower than expected on Graviton | x86 emulation / wrong JDK | Native arm64 JDK/Node binary |
| Docker pull wrong arch | Single-platform image | Manifest list with buildx |
| Native module fail (node-gyp) | Prebuilt binary x86 only | Compile on arm64 CI |

## Mistakes to Avoid
- **Mistake:** Assuming SIMD parity with x86
- **Mistake:** **Apple Rosetta**
- **Mistake:** **Memory model**
- **Mistake:** **32-bit ARM (armv7)** legacy — new server work is AArch64

## Pros/Cons or Trade-offs
- **Trade-off:** Don't pick ARM for workload depending on proprietary x86-only libs without port plan.
- **Trade-off:** Desktop gaming GPU stack — still x86-heavy; ARM choice is workload-specific.
