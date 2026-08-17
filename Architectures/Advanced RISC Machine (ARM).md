[[Operating System/base clock speed]] [[Operating System/Single Instruction, Multiple Data (SIMD)]] [[Operating System/context switching]] [[AWS/AWS EC2]]

# Advanced RISC Machine (ARM)

> ARM (Advanced RISC Machine) — RISC load/store CPUs; AArch64 is the modern 64-bit server and mobile baseline.





## Interview Relevance
ARM/AArch64 questions check RISC load/store thinking, calling conventions, and why cloud graviton/apple silicon matter for builds.

## Sources
- [Arm Architecture Reference Manual](https://developer.arm.com/documentation) — deep-dive
- [Wikipedia — ARM architecture family](https://en.wikipedia.org/wiki/ARM_architecture_family) — overview

## Key Concepts
**ARM** (Advanced RISC Machine) uses **Reduced Instruction Set Computing**: simple instructions, register-register operations, explicit load/store to memory. **AArch64** (64-bit) is the modern server and mobile baseline.

```
Program Counter (PC) → fetch instruction → decode → execute → writeback
                              │
ARM pipeline: PC may read as current + offset (+8 bytes in AArch64 EL0 debug)
```

| vs x86 | ARM tendency |
|--------|--------------|
| Instruction density | Fixed 32-bit (A64); compact Thumb history on 32-bit ARM |
| Power | Better perf/W — Apple Silicon, Graviton |
| Ecosystem | Mobile first; Linux server growth (AWS Graviton) |

**PC quirk:** When reading PC in debug/asm, value often **points ahead** of current instruction due to pipeline prefetch (commonly **PC + 8** in ARM state) — branch/link math must account for this.

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
- Same application, ~20–40% better price-performance for many workloads versus x86

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

## Pros/Cons or Trade-offs
- **Trade-off:** Don't pick ARM for workload depending on proprietary x86-only libs without port plan.
- **Trade-off:** Desktop gaming GPU stack — still x86-heavy; ARM choice is workload-specific.

## Mistakes to Avoid
- Assuming SIMD parity with x86 — NEON ≠ AVX512; vectorize carefully in crypto/video code.
- **Apple Rosetta** — x86 binary translated; perf testing needs native arm64 build.
- **Memory model** — weaker ordering than x86; lock-free code needs barriers.
- **32-bit ARM (armv7)** legacy — new server work is AArch64.
