#!/usr/bin/env python3
"""Rebuild all Operating System/*.md notes per AGENT_NOTE_RULES.md."""

from pathlib import Path

ROOT = Path("/workspace/Operating System")

NOTES: dict[str, str] = {}

def note(path: str, content: str) -> None:
    NOTES[path] = content.strip() + "\n"

# --- Batch 1: storage, hardware interfaces, assembly, buffers ---

note("abstract storage location.md", """
[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[file descriptors]] [[logical partitions]]

# Abstract storage location

> An abstract storage location is any addressable place where bytes live — file, block device, memory-mapped region, or cloud object — without naming the physical medium underneath.

Operating systems and applications rarely talk to spinning platters or NAND cells directly. They talk to **abstract locations**: paths, volume identifiers, logical block addresses, or handles returned by the kernel. The abstraction hides geometry, vendor firmware, and RAID layout while still exposing read, write, seek, and durability semantics.

## Why abstraction matters

| Layer | What the caller sees | What is hidden |
|-------|----------------------|----------------|
| Application | `open("/var/log/app.log")` | inode, extents, SSD wear leveling |
| Database | tablespace file or raw device | partition table, LVM striping |
| Container | bind-mounted path in a namespace | host filesystem, copy-on-write graph driver |
| Cloud VM | EBS volume or persistent disk | hypervisor storage backend |

Abstraction lets the same program run on a laptop SSD, a SAN LUN, or a network file system. It also centralizes policy: permissions, quotas, encryption, and caching apply at the abstract boundary ([[file descriptors]], [[Buffer cache]]).

## How locations are named

**Path names** resolve through a virtual file system layer to an inode and backing store. **Block devices** (`/dev/nvme0n1p2`) expose fixed-size sectors; user space often still uses a filesystem on top. **Memory-mapped files** map an abstract file range into the process address space — the same cached pages may back both `read()` and a direct load instruction.

Persistent storage notes tie the idea to concrete boot and layout topics: [[MBR]], [[logical partitions]], [[Persistent Block Storage]].

## Durability is not automatic

Writing to an abstract location usually lands in a cache first ([[Buffer cache]], page cache). The bytes are visible to readers on the same machine, but survive power loss only after the kernel and device flush dirty data — see [[fsync]] and [[Persistent Block Storage]].

## Sources

- Linux kernel documentation: [Page Cache](https://docs.kernel.org/mm/page_cache.html)
- Tanenbaum & Bos, *Modern Operating Systems* — file system and I/O abstraction layers
- Wikipedia: [Computer data storage](https://en.wikipedia.org/wiki/Computer_data_storage)
""")

note("analog interface.md", """
[[Operating System]] [[bus]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Electronic Control Unit (ECU)]]

# Analog interface

> An analog interface moves continuously varying physical quantities — voltage, current, pressure — across the boundary between the real world and digital logic the operating system can schedule.

Digital computers store discrete bits. Sensors and actuators in the physical world are analog. An **analog interface** (often an ADC or DAC plus conditioning circuitry) samples or drives those signals so firmware and drivers can treat them as numbers.

## Signal path

```txt
Physical quantity → sensor → amplifier/filter → ADC → digital bus → driver → user space
User command      → DAC  → actuator → physical effect
```

On a general-purpose PC, analog work often lives on dedicated chips (audio codec, temperature sensor on the SMBus). On embedded targets such as an [[Electronic Control Unit (ECU)]], analog I/O may be the primary reason the microcontroller exists.

## Operating system view

The kernel exposes analog-backed devices as **character devices**, **Industrial I/O (IIO)** channels, or platform-specific ioctls. User space reads structured samples (`read()`, `read()` on `/dev/iio:device0`) rather than raw pin voltages. Timing and sample rate are constrained by the [[bus]] bandwidth and interrupt latency — not by how fast a loop can spin in Python.

## Contrast with digital I/O

[[Data Direction Register (DDR)]] style GPIO is on/off. Analog interfaces deal with resolution (bits of ADC), sampling rate, noise, and calibration. Choosing the wrong interface type — treating a slow analog sensor as a digital edge — loses information or adds aliasing.

## Sources

- Wikipedia: [Analog-to-digital converter](https://en.wikipedia.org/wiki/Analog-to-digital_converter)
- Linux kernel documentation: [Industrial I/O](https://docs.kernel.org/driver-api/iio/index.html)
- Horowitz & Hill, *The Art of Electronics* — ADC/DAC fundamentals
""")

note("assembly language.md", """
[[Operating System]] [[opcode]] [[linker]] [[Stack Frame]] [[stack pointer]] [[system call]]

# Assembly language

> Assembly language is human-readable mnemonics for machine instructions — the lowest level most developers use before silicon, and the layer where syscalls, stacks, and calling conventions become visible.

Each CPU family defines an **instruction set architecture (ISA)**. Assembly maps one mnemonic (for example `mov`, `syscall`, `ret`) to one or more machine **opcodes** ([[opcode]]). An **assembler** turns `.s` files into object code; the [[linker]] combines objects into an executable [[OS program]].

## Relationship to the operating system

User programs cannot open a disk or map memory by writing to ports directly (on modern protected systems). They load arguments into registers, execute a syscall instruction, and trap into the kernel ([[system call]]). Debugging at this layer shows exactly which registers hold file descriptors and error codes.

```txt
; simplified x86-64 write(1, buf, len) — illustrative
mov    rax, 1          ; __NR_write
mov    rdi, 1          ; stdout
; rsi = buf, rdx = len
syscall
```

## Stack and procedures

Function calls push a [[Stack Frame]]: return address, saved registers, locals. The [[stack pointer]] must stay aligned; corruption here produces impossible returns — see [[Stack trace]]. Compilers generate assembly (or LLVM IR lowered to machine code); hand-written assembly remains common in boot loaders, kernels, and hot paths.

## When you still meet it

- Reading crash dumps and [[Stack trace]] output
- Boot and firmware paths ([[Boot/UEFI]], [[MBR]] first-stage loaders)
- Performance tuning where the compiler’s choices matter
- Security research on shellcode and return-oriented programming

## Sources

- Intel® 64 and IA-32 Architectures Software Developer’s Manual — instruction set reference
- AMD64 Architecture Programmer’s Manual
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective*
- Wikipedia: [Assembly language](https://en.wikipedia.org/wiki/Assembly_language)
""")

note("atomic ring buffer.md", """
[[Operating System]] [[Rolling Buffer]] [[kernel ring buffer]] [[thread-safe queue]] [[mutexes]] [[multi-threaded]]

# Atomic ring buffer

> A ring buffer stores a fixed-capacity stream by wrapping a read index and write index around a circular array — atomics let one producer and one consumer update those indices without a lock.

A **ring buffer** (circular buffer) avoids shifting elements: when the write index reaches the end, it wraps to zero. **Atomic** operations (C11 `atomic_load`/`atomic_store`, or kernel `READ_ONCE`/`WRITE_ONCE` with memory barriers) publish index updates so the other side sees a consistent snapshot.

## Single-producer, single-consumer (SPSC)

The classic lock-free pattern:

```txt
     read_idx ──► [ | | | | | ] ◄── write_idx
                    buffer[N]
```

- Producer advances `write_idx` after storing data.
- Consumer advances `read_idx` after reading data.
- Full when `(write + 1) % N == read`; empty when `write == read`.

Only one writer and one reader may touch each index without additional synchronization. Multiple producers require [[mutexes]], semaphores ([[semaphores]]), or a [[thread-safe queue]].

## Where it appears

| Use | Example |
|-----|---------|
| Kernel logging | [[kernel ring buffer]] (`dmesg`) |
| Audio / DSP | Sample streams between interrupt and user thread |
| IPC | Pipe-like shared-memory channels |
| Networking | NIC driver descriptor rings |

## Failure modes

- **Overrun** — producer faster than consumer; oldest data is dropped or the write blocks.
- **Torn reads** — without proper barriers, consumer sees new index but old slot contents (fix: store data before publishing index).
- **False sharing** — read and write indices on the same cache line ping-pong between cores.

Compare with a generic [[Rolling Buffer]] used for logging semantics and [[right buffer]] sizing for latency versus memory.

## Sources

- Linux kernel: `include/linux/kfifo.h`, `lib/kfifo.c`
- Lamport, “Concurrent Reading and Writing” (ring buffer foundations)
- Wikipedia: [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer)
""")

note("base clock speed.md", """
[[Operating System]] [[SMT threads]] [[TDP]] [[CPU IO Bound Task]] [[context switching]]

# Base clock speed

> Base clock speed is the guaranteed steady-state frequency of a CPU core under nominal thermal and power limits — not the short turbo burst you see in marketing.

Modern processors expose **base** and **maximum turbo** frequencies (GHz). The **base clock** is the speed the vendor certifies when all cores run a typical workload within thermal design power ([[TDP]]). Turbo raises frequency when headroom exists; under sustained load the core often settles near base or an intermediate all-core frequency.

## What actually sets frequency

```txt
Workload demand → OS scheduler places threads on cores
                → hardware P-states / CPPC choose frequency
                → thermal and power limits (TDP, PL1/PL2) cap or throttle
```

Linux exposes this through `cpufreq` governors (`performance`, `powersave`, `schedutil`), `/proc/cpuinfo`, and tools like `turbostat`. Container CPU quotas ([[cgroup (Control Group)]]) limit effective compute even when the hardware could turbo higher.

## Why it matters for systems work

- **[[CPU IO Bound Task]]** — an I/O-bound service rarely needs peak GHz; wrong-sizing leads to paying for idle turbo headroom.
- **[[context switching]]** — higher frequency reduces time per quantum but does not remove scheduler overhead.
- **[[SMT threads]]** — two logical CPUs share one core’s execution units; both compete for the same frequency and cache budget.

Base clock is a hardware specification; observed performance still depends on memory latency, disk ([[disk IOPS]]), and lock contention ([[mutexes]]).

## Sources

- Intel® 64 Architecture Software Developer’s Manual — power management
- Linux kernel documentation: [CPUFreq](https://docs.kernel.org/admin-guide/pm/cpufreq.html)
- Wikipedia: [CPU multiplier](https://en.wikipedia.org/wiki/CPU_multiplier), [Dynamic frequency scaling](https://en.wikipedia.org/wiki/Dynamic_frequency_scaling)
""")

note("Blocking.md", """
[[Operating System]] [[Blocking Vs Non-Blocking]] [[non-blocking]] [[system call]] [[Thread]] [[context switching]]

# Blocking

> A blocking operation holds the calling thread until the kernel can complete work — disk read, mutex, sleep — and that wait usually costs a context switch.

When a [[Thread]] invokes a **blocking** [[system call]] such as `read()` on an empty pipe or `accept()` with no connection, the kernel marks the thread blocked, schedules another runnable thread, and later wakes the caller when data arrives. From the application’s perspective the call does not return until the event happens (or a signal interrupts it).

## Blocking versus readiness

| Mode | If data not ready | Thread state |
|------|-------------------|--------------|
| Blocking (default) | Waits inside kernel | Blocked → [[context switching]] |
| [[non-blocking]] | Returns immediately with `EAGAIN` | Stays runnable |

Blocking code is simple to reason about: sequential reads and writes mirror human workflow. At high concurrency, thousands of blocked threads consume stack memory and scheduler bookkeeping — the classic motivation for event loops and [[Epoll]].

## Common blocking points

- Disk and network I/O waiting on media or peer
- `pthread_mutex_lock` when the lock is held
- `futex` waits inside glibc mutexes ([[mutexes]])
- `poll()` / `select()` without timeout

## Design tension

**When blocking is fine:** worker count matches concurrent operations (small server, batch job, thread pool sized to cores).

**When blocking hurts:** one thread must multiplex many connections — switch to non-blocking I/O and a reactor, or use async runtimes that hide blocking in a pool.

See [[Blocking Vs Non-Blocking]] for side-by-side trade-offs.

## Sources

- Kerrisk, *The Linux Programming Interface* — file I/O and threads
- Stevens & Rago, *Advanced Programming in the UNIX Environment*
- Wikipedia: [Blocking (computing)](https://en.wikipedia.org/wiki/Blocking_(computing))
""")

note("Blocking Vs Non-Blocking.md", """
[[Operating System]] [[Blocking]] [[non-blocking]] [[Epoll]] [[system call]] [[CPU IO Bound Task]]

# Blocking Vs Non-Blocking

> Blocking waits inside the kernel until I/O is ready; non-blocking returns immediately and pushes the wait into your event loop — choose based on concurrency shape, not ideology.

Both modes are properties of **how a file descriptor (or socket) is configured**, combined with how the [[Thread]] model uses them. They are not separate “kinds” of network stack.

## Comparison

| Aspect | Blocking | Non-blocking |
|--------|----------|--------------|
| Call behavior | Thread sleeps until ready | Returns `EAGAIN` / `EWOULDBLOCK` if not ready |
| Code style | Linear, one thread per flow | State machine or callback / async |
| Scalability | Thread count ≈ concurrent waits | Few threads + [[Epoll]] / kqueue |
| Latency under load | Scheduler and stack overhead | Lower thread overhead; complex app logic |
| Error handling | Simple return codes | Must retry on `EINTR` and `EAGAIN` |

## Typical architectures

```txt
Blocking model:
  Thread 1 ── accept ── read ── write ── close
  Thread 2 ── accept ── read ── write ── close
  (N threads for N idle clients)

Non-blocking model:
  Event loop ── epoll_wait ── dispatch read/write on ready fds
  (few threads, many connections)
```

## Hybrid patterns

Thread pools handle **blocking** disk or database calls while the accept loop stays non-blocking. Runtimes (Node.js, Go) multiplex many logical tasks onto fewer OS threads — know which layer is blocking ([[CPU IO Bound Task]]).

Setting non-blocking mode:

```c
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);
```

## Sources

- Kerrisk, *The Linux Programming Interface* — non-blocking I/O, `select`, `poll`, `epoll`
- Linux `fcntl(2)`, `epoll(7)` manual pages
- Wikipedia: [C10k problem](https://en.wikipedia.org/wiki/C10k_problem)
""")

note("Boot/UEFI.md", """
[[Operating System]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[Persistent Block Storage]] [[inittramfs]]

# UEFI

> UEFI (Unified Extensible Firmware Interface) is modern PC firmware that initializes hardware, reads boot entries from NVRAM, and loads signed EFI applications from the EFI System Partition — replacing the 446-byte MBR boot sector chain.

After power-on, the CPU starts firmware at a reset vector. **UEFI** runs in 32- or 64-bit mode with drivers, protocols, and a **boot manager** defined by the UEFI specification. The boot manager consults variables such as `BootOrder` and `Boot####` to choose an OS loader (for example `\\EFI\\ubuntu\\shim.efi` → GRUB → Linux kernel).

## Boot flow (simplified)

```txt
Power-on → SEC/PEI/DXE (platform init) → BDS boot manager
         → load .efi from ESP (EFI System Partition, FAT32, GPT)
         → optional Secure Boot signature check
         → OS loader loads kernel + [[inittramfs]]
         → kernel takes over (long mode on x86-64)
```

## Versus legacy BIOS + MBR

| Topic | Legacy BIOS | UEFI |
|-------|-------------|------|
| Partition table | [[MBR]] (2 TiB limit) | GPT (large disks) |
| Boot code location | First sector boot sector | Files on ESP |
| Security | No standard Secure Boot | Secure Boot, measured boot (TPM) |
| Handoff mode | 16-bit real mode chain | Protected/long mode with tables |

Many machines ship **UEFI with CSM** (Compatibility Support Module) to boot old MBR images — see [[Boot/UEFI (2)]] for practical firmware menu behavior.

## Operations relevance

- Reinstalling boot loaders requires mounting the ESP (`/boot/efi`).
- Dual-boot means multiple NVRAM entries, not only an “active” partition flag.
- Cloud images are often UEFI-GPT; bare-metal automation must align partition layout with firmware mode.

Related: [[Boot/Extensible Firmware interface (efi)]] (EFI naming history), [[Linux/management/grub]].

## Sources

- UEFI Specification 2.10 — [Boot Manager](https://uefi.org/specs/UEFI/2.10/03_Boot_Manager.html)
- Wikipedia: [UEFI](https://en.wikipedia.org/wiki/UEFI)
- Microsoft Learn: UEFI firmware documentation
""")

note("Boot/UEFI (2).md", """
[[Operating System]] [[Boot/UEFI]] [[Boot/Extensible Firmware interface (efi)]] [[MBR]] [[MBR(Master Boot Record)]]

# UEFI (2)

> Practical UEFI — firmware setup menus, ESP layout, Secure Boot, and the CSM fallback that still boots legacy MBR disks when “UEFI-only” fails.

This note complements [[Boot/UEFI]] with field operations: what you touch when a machine “will not boot” after disk clone, dual-boot, or RAID changes.

## Firmware setup concepts

- **Boot mode:** UEFI native versus Legacy/CSM — mismatch with partition scheme (GPT vs [[MBR]]) produces “no bootable device.”
- **Secure Boot:** when enabled, unsigned or unknown boot loaders fail unless enrolled (shim + MOK, or custom keys).
- **Boot order:** NVRAM entries point to `.efi` paths, not only disk order.
- **Fast Boot / Ultra Fast:** may skip USB enumeration — affects rescue USB keys.

## EFI System Partition (ESP)

- FAT32, flagged ESP on GPT, typically 100–550 MiB.
- Holds vendor-specific paths: `EFI/Microsoft/Boot`, `EFI/ubuntu`, `EFI/BOOT/BOOTX64.EFI`.
- Clone migrations must copy ESP **and** re-register NVRAM entries or run `efibootmgr`.

## When CSM still matters

Old images, some PXE chains, and MBR-only USB installers rely on **CSM** to emulate BIOS INT 13h disk access. Pure UEFI paths load PE/COFF binaries directly — no 446-byte stage in LBA 0.

```txt
UEFI-native:  GPT + ESP + .efi loader
Legacy/CSM:   MBR active partition + boot sector chain → GRUB/Windows VBR
```

## Recovery checklist

1. Confirm firmware mode matches disk label type (GPT/UEFI or MBR/legacy).
2. Mount ESP; verify `BOOTX64.EFI` or distribution shim exists.
3. `efibootmgr -v` — correct disk UUID and `.efi` path.
4. Disable Secure Boot temporarily to isolate signature issues.
5. For Linux, reinstall grub-efi to ESP from chroot.

## Sources

- UEFI Specification 2.10 — Boot Manager, Secure Boot
- Rod Smith, *Managing EFI Boot Loaders* (rEFInd documentation)
- Wikipedia: [UEFI](https://en.wikipedia.org/wiki/UEFI), [EFI System Partition](https://en.wikipedia.org/wiki/EFI_System_PARTITION)
""")

note("Boot/Extensible Firmware interface (efi).md", """
[[Operating System]] [[Boot/UEFI]] [[Boot/UEFI (2)]] [[PCI (Peripheral Component Interconnect)]]

# Extensible Firmware interface (efi)

> EFI (Extensible Firmware Interface) is Intel’s 1990s firmware specification that evolved into UEFI — same core idea: modular drivers, GPT disks, and PE/COFF boot applications instead of BIOS interrupt chains.

**EFI** introduced a driver model, boot services/runtime services split, and cross-platform abstractions. **UEFI** (Unified EFI) is the industry-maintained successor managed by the UEFI Forum. In conversation “EFI partition” and “UEFI boot” usually mean the modern unified spec ([[Boot/UEFI]]).

## EFI services (conceptual)

| Phase | Role |
|-------|------|
| Boot Services | Memory map, protocol handles, load images — torn down when OS calls `ExitBootServices` |
| Runtime Services | Small subset survives into OS (variables, clock, reset) |

Boot loaders query GOP (graphics), block I/O, and simple file system protocols to read the kernel from disk.

## Naming in the field

- **ESP** — EFI System Partition on GPT.
- **.efi files** — PE32+ executables the firmware runs directly.
- **OVMF** — open-source UEFI firmware for QEMU/KVM guests.

Legacy **BIOS** used 16-bit real-mode interrupt handlers; EFI/UEFI runs flat protected/long mode with tables describing hardware — closer to how an [[OS program]] expects memory.

## Sources

- UEFI Forum — [Specifications](https://uefi.org/specifications)
- Wikipedia: [Unified Extensible Firmware Interface](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface) (EFI history)
- Intel Platform Innovation Framework for EFI (pre-UEFI documentation archive)
""")

note("Browser memory.md", """
[[Operating System]] [[Heap memory]] [[buffer]] [[RAM and Swap memory]] [[OOM (Linux Out Of Memory)]]

# Browser memory

> A browser is a multi-process user-space operating environment — each tab’s JavaScript heap, DOM, GPU buffers, and disk cache compete for the same machine RAM the kernel accounts in [[RAM and Swap memory]].

Chromium-derived browsers split **browser**, **GPU**, **network**, and **renderer** processes. A heavy web app can consume gigabytes across:

- **JavaScript heap** — objects, closures, typed arrays ([[Heap memory]] semantics at user level).
- **DOM / layout** — C++ trees in the renderer, not visible to JS heap profilers alone.
- **Image and canvas buffers** — large contiguous allocations, sometimes GPU-resident.
- **HTTP cache / code cache** — memory-backed with eviction policies similar to [[Buffer cache]].
- **Shared memory** — IPC between processes ([[Inter Process Communication]], [[shared memory]]).

## Pressure and failure

When system memory is tight, Linux reclaims page cache and may swap anonymous pages. The browser may discard tab backgrounds or kill renderer processes before the kernel’s [[OOM (Linux Out Of Memory)]] killer selects a system daemon — but runaway tabs can still trigger global OOM.

Developer tools (`about:memory`, Performance heap snapshots) measure **JS heap** only; use OS tools (`ps`, `smem`, `/proc/PID/smaps_rollup`) for true RSS.

## Engineering implications

- Large ArrayBuffers and WebAssembly linear memory bypass typical GC pacing — spikes look like native leaks.
- Service workers and caches persist across navigations; memory is not freed on `location.href` alone.
- Container limits ([[cgroup (Control Group)]]) cap entire browser cgroup RSS for kiosk or CI runners.

## Sources

- Chromium design docs — [Multi-process Architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/)
- Google developers — memory tooling for Chrome
- Wikipedia: [Web browser engine](https://en.wikipedia.org/wiki/Web_browser_engine)
""")

note("Buffer cache.md", """
[[Operating System]] [[buffer]] [[buffer head]] [[fsync]] [[file descriptors]] [[Persistent Block Storage]]

# Buffer cache

> On Linux, the buffer cache is not a separate cache anymore — file and block data live in the unified page cache, with buffer heads describing how pages map to disk blocks.

Historically the kernel kept two caches: **page cache** for file contents and **buffer cache** for block-device I/O. Since Linux 2.4 they merged: all file-backed and block-backed paths share the **page cache** ([[kernel subsystem]] memory management). People still say “buffer cache” when discussing dirty blocks, writeback, and `sync` behavior.

## Read path

```txt
read() → lookup inode page in page cache → hit: copy to user
                                        → miss: read disk, populate cache, then copy
```

Readahead prefetches sequential pages. Memory is dynamic — unused cache pages are reclaimed under pressure before OOM.

## Write path and durability

Writes mark pages **dirty** in RAM and return quickly. Flushing to [[Persistent Block Storage]] happens via:

- Background **writeback** (`pdflush` / `bdi` threads)
- Explicit `sync()`, `fsync()` ([[fsync]]), `msync()`

Power loss before flush means data existed only in cache — databases depend on fsync semantics.

## Buffer heads

A [[buffer head]] (`struct buffer_head`) ties a logical disk block to a page cache page for block-layer I/O. Higher-level file I/O usually goes through `address_space` and folios; buffer heads remain relevant for some block and filesystem paths.

## Inspection

```bash
free -h              # "buff/cache" line
grep -E 'Dirty|Writeback' /proc/meminfo
echo 3 | sudo tee /proc/sys/vm/drop_caches   # lab only — drops clean cache
```

## Sources

- Linux kernel documentation: [Page Cache](https://docs.kernel.org/mm/page_cache.html)
- Robert Love, *Linux Kernel Development* — Chapter on page cache and writeback
- Thomas-Krenn Wiki — Linux Page Cache Basics
""")

note("buffer.md", """
[[Operating System]] [[Buffer cache]] [[buffer head]] [[buffer lifecycle]] [[buffer flags]] [[multiple levels of buffering]]

# Buffer

> A buffer is a temporary memory region that decouples producers and consumers — smoothing speed mismatches between CPU, kernel, network, and disk.

Buffers appear at every layer: user-space `stdio` arrays, socket send buffers, disk controller queues, and the kernel [[Buffer cache]]. The pattern is the same: **accumulate data**, **batch transfer**, **hide latency**.

## Why layers stack

```txt
App fwrite buffer → socket SO_SNDBUF → NIC ring → switch → disk queue → NAND page program
```

Each [[multiple levels of buffering]] adds latency but improves throughput. Tuning one layer without others shifts bottlenecks — shrinking TCP buffers under a bursty writer causes more syscalls ([[system call]]).

## Buffer versus cache

| Term | Intent |
|------|--------|
| Buffer | Absorb timing differences; often drained in order |
| Cache | Keep copies for faster reuse; eviction policies vary |

The Linux page cache is caching, but block I/O still uses buffer descriptors ([[buffer head]]) when bridging filesystem pages and LBA addresses.

## Lifecycle

Allocation, fill, flush, and release follow a predictable cycle — see [[buffer lifecycle]]. Flags on block buffers ([[buffer flags]]) record dirty, locked, or mapped state for the kernel block layer.

Ring-style buffers ([[Rolling Buffer]], [[atomic ring buffer]], [[kernel ring buffer]]) specialize streaming and logging workloads.

## Sources

- Tanenbaum, *Modern Operating Systems* — I/O buffering
- Stevens, *UNIX Network Programming* — socket buffers
- Linux kernel: `mm/filemap.c`, block layer buffer documentation
""")

note("buffer head.md", """
[[Operating System]] [[Buffer cache]] [[buffer flags]] [[buffer lifecycle]] [[Persistent Block Storage]]

# Buffer head

> A buffer head is the kernel’s descriptor linking one logical disk block to a page in the page cache — the legacy bridge between the block layer and memory management.

`struct buffer_head` (and modern helpers built on folios) answers: **which page**, **which block number**, **which device**, and **what state** (dirty, uptodate, locked). File systems and the block layer use buffer heads when I/O is expressed in fixed **sectors** rather than whole file pages.

## Role after the page-cache merge

Since the buffer cache merged into the [[Buffer cache]] (page cache), buffer heads do not represent a second copy of data — they **index** a slice of a cached page. Multiple buffer heads can reference different blocks within the same page.

## State machine (conceptual)

```txt
allocate bh → map to page → read I/O fills → mark uptodate
           → modify → set dirty ([[buffer flags]])
           → writeback → clear dirty → unlock
```

Concurrent access relies on locking buffer heads and page locks; races here cause filesystem corruption — why `fsync` and journal ordering matter ([[fsync]]).

## User-space visibility

Normal applications use paths and [[file descriptors]], not buffer heads. They matter when reading **kernel** or **filesystem** source, analyzing `block` layer traces, or debugging tunefs/block-size mismatches on [[Persistent Block Storage]].

## Sources

- Linux kernel documentation: [Buffer Head API](https://docs.kernel.org/core-api/buffer.html)
- Robert Love, *Linux Kernel Development* — buffer heads and page cache
- Wikipedia: [Buffer cache](https://en.wikipedia.org/wiki/Buffer_cache)
""")

note("buffer flags.md", """
[[Operating System]] [[buffer head]] [[Buffer cache]] [[buffer lifecycle]] [[fsync]]

# Buffer flags

> Buffer flags are kernel bitfields on a buffer head that record whether a block is dirty, locked, mapped, or mid-writeback — the block layer’s state machine in compact form.

Each [[buffer head]] carries flags such as **`BH_Dirty`** (must reach disk), **`BH_Uptodate`** (cache matches media), **`BH_Lock`** (I/O in progress), and **`BH_Mapped`** (associated with a disk block). Together they prevent double writes, torn reads, and use-after-free during writeback.

## Common flags (conceptual)

| Flag role | Meaning if set |
|-----------|----------------|
| Dirty | RAM newer than backing store — needs flush |
| Uptodate | Valid data for this block |
| Lock | Holder is performing I/O; others wait |
| Mapped | Block number bound to this buffer |

Flags interact with page dirty bits in the [[Buffer cache]]: filesystem code sets dirty when metadata or data changes; **`sync`** and [[fsync]] paths walk dirty structures and schedule I/O.

## Why operators rarely touch them

These flags exist in kernel memory. User space observes effects through latency (`iostat`, slow commits) and durability guarantees, not flag dumps. Debugging uses `tracepoints` / `block` subsystem trace or `crash` on vmcores.

## Sources

- Linux kernel: `include/linux/buffer_head.h`
- Linux kernel documentation: [Buffer Head API](https://docs.kernel.org/core-api/buffer.html)
- Understanding the Linux Kernel (Bovet & Cesati) — block I/O chapter
""")

note("buffer lifecycle.md", """
[[Operating System]] [[buffer]] [[buffer head]] [[buffer flags]] [[Buffer cache]] [[multiple levels of buffering]]

# Buffer lifecycle

> A kernel or application buffer moves through allocate → fill → optionally dirty → flush → reclaim — each transition has failure modes if the next stage is slower than the producer.

## Typical kernel block buffer

```txt
1. Allocate buffer head + attach to page ([[buffer head]])
2. Read or write fills memory — set uptodate / dirty ([[buffer flags]])
3. Background or explicit flush schedules I/O toward disk
4. I/O completion clears dirty, unlocks
5. Page reclaimed under memory pressure if clean
```

User-space buffers (socket, `stdio`) follow the same rhythm without buffer heads: malloc → append → `write()` → free or reuse.

## Interaction with stacked buffering

[[multiple levels of buffering]] mean a logical “flush” at one layer does not flush lower layers. `fflush()` does not [[fsync]]; TCP `close()` does not guarantee the peer persisted data.

## Reclaim and pressure

Clean [[Buffer cache]] pages are cheap to drop. Dirty pages must be written or discarded with care — writeback throttling prevents flooding slow disks. Under OOM, the kernel prefers dropping cache before killing processes.

## Questions for design reviews

- What happens on power loss mid-lifecycle?
- Which layer’s full buffer blocks the producer?
- Is there a bound on buffered bytes (backpressure)?

## Sources

- Linux kernel: `mm/page-writeback.c`, block layer writeback
- Robert Love, *Linux Kernel Development*
- Tanenbaum, *Modern Operating Systems* — I/O and buffering
""")

note("bus.md", """
[[Operating System]] [[system bus]] [[PCI (Peripheral Component Interconnect)]] [[Data Direction Register (DDR)]]

# Bus

> A bus is a shared communication pathway — address, data, and control lines — that lets the CPU, memory, and devices exchange bytes under a defined protocol.

Early machines used parallel **system buses**. Modern PCs nest specialized buses: processor ↔ memory links (QPI/UPI), chipset **PCIe** ([[PCI (Peripheral Component Interconnect)]]), USB, I2C/SMBus for sensors. Operating systems discover devices via enumeration (ACPI tables, PCI config space) and attach **drivers** that speak each protocol.

## Bus versus network

Both move packets, but a **bus** is local, low-latency, and electrically shared or switched inside one machine. Latency and ordering rules differ from Ethernet ([[TCP]] rides on NICs attached via PCIe).

## Embedded view

Microcontrollers expose GPIO with a [[Data Direction Register (DDR)]] per port — pin direction on a simple parallel bus. [[Electronic Control Unit (ECU)]] firmware bit-bangs or uses CAN/LIN buses rather than PCIe.

## Performance symptoms

Bus contention shows as **stalls**: DMA fighting CPU memory bandwidth, GPU copying over PCIe, or too many small MMIO reads. Tools: `perf`, `lspci -vv`, hardware counters — not only application profilers.

See [[system bus]] for the CPU–memory–I/O triangle.

## Sources

- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*
- Wikipedia: [Computer bus](https://en.wikipedia.org/wiki/Computer_bus)
- Linux: `lspci`, PCI subsystem documentation
""")

note("system bus.md", """
[[Operating System]] [[bus]] [[PCI (Peripheral Component Interconnect)]] [[base clock speed]] [[Persistent Block Storage]]

# System bus

> The system bus is the backbone that connects the CPU, main memory, and I/O controllers — every syscall that touches disk or network eventually moves bytes across these links.

Classic model (**Von Neumann**):

```txt
     ┌─────────┐   address/data/control   ┌──────────┐
     │   CPU   │◄────────────────────────►│   RAM    │
     └────┬────┘                          └──────────┘
          │
          ▼
     I/O bridge → [[PCI (Peripheral Component Interconnect)]] / USB / NVMe
```

## Modern wrinkles

- **NUMA:** multiple memory controllers — local versus remote DRAM latency differs.
- **Cache coherence:** CPUs snoop bus traffic (or directory protocols) to keep caches consistent — relevant to [[mutexes]] false sharing.
- **DMA:** devices read/write RAM without CPU byte loops — driver buffers in [[Buffer cache]].

The [[bus]] note covers generic concepts; **system bus** emphasizes the CPU-centric path from instruction fetch to [[Persistent Block Storage]] I/O.

## Sources

- Hennessy & Patterson, *Computer Architecture*
- Wikipedia: [System bus](https://en.wikipedia.org/wiki/System_bus), [Front-side bus](https://en.wikipedia.org/wiki/Front-side_bus)
""")

note("cgroup (Control Group).md", """
[[Operating System]] [[process]] [[RAM and Swap memory]] [[IPC namespace]] [[Linux/management/Linux cgroup]]

# cgroup (Control Group)

> Control groups (cgroups) are the Linux kernel mechanism that limits and accounts for CPU, memory, I/O, and pids — the enforcement layer behind containers and systemd slices.

**Cgroups v2** (unified hierarchy) attach each process to groups with limits such as:

| Controller | Limits |
|------------|--------|
| `cpu` | Quota, weight, burst |
| `memory.max` | RSS + cache charged to cgroup — OOM kill inside group |
| `io` | Bandwidth on block devices |
| `pids.max` | Fork bomb containment |

Docker, Kubernetes, and systemd (`system.slice`, `user.slice`) all write cgroup files under `/sys/fs/cgroup/`.

## Interaction with namespaces

[[IPC namespace]], [[UTS namespace]], and PID/network namespaces **isolate view**; cgroups **isolate resources**. A pod is typically namespaces + cgroup limits together.

## Debugging

```bash
systemd-cgls
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.current
cat /sys/fs/cgroup/.../cpu.stat   # nr_throttled → [[context switching]] pressure
```

See also [[Linux/management/Linux cgroup]] and [[logical partitions]] (conceptual analogy: dividing machine resources).

## Sources

- Linux kernel documentation: [Control Groups v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- systemd.resource-control(5)
- Wikipedia: [Cgroups](https://en.wikipedia.org/wiki/Cgroups)
""")

note("context switching.md", """
[[Operating System]] [[Thread]] [[multi-threaded]] [[SMT threads]] [[mutexes]] [[thread pool]]

# Context switching

> A context switch saves one thread’s CPU registers and restores another’s — the scheduler tax that shows up as `cs` in vmstat when you have more runnable work than cores can serve cleanly.

Triggered by timer preemption, blocking [[system call]], lock contention, or explicit yield. **Process switch** (different address space) costs more than **thread switch** within one process because MMU state and TLB entries may change.

## Costs

- **Direct:** microseconds in kernel scheduler paths.
- **Indirect:** cold caches and branch predictors — often dominates on hot loops.

## Measurement

```bash
vmstat 1          # cs column
pidstat -w 1      # voluntary vs involuntary
perf stat -e context-switches,cpu-migrations -p PID
```

## Mitigation patterns

- Size [[thread pool]] to ~cores for CPU-bound work.
- Prefer event loops for many idle connections ([[non-blocking]], [[Epoll]]).
- Avoid oversubscribing [[SMT threads]] with lock-heavy workers.

[[cgroup (Control Group)]] CPU throttling increases involuntary switches under quota pressure.

## Sources

- Silberschatz, Galvin & Gagne, *Operating System Concepts* — CPU scheduling
- Linux kernel documentation: [Scheduler](https://docs.kernel.org/scheduler/index.html)
- Wikipedia: [Context switch](https://en.wikipedia.org/wiki/Context_switch)
""")

note("CPU IO Bound Task.md", """
[[Operating System]] [[Blocking]] [[thread pool]] [[disk IOPS]] [[context switching]] [[multi-threaded]]

# CPU IO Bound Task

> A task is I/O-bound when it spends most of its time waiting on disk, network, or locks held by others — not executing instructions; sizing threads and hardware differs completely from CPU-bound work.

## Bound type drives design

| Profile | Dominant wait | Thread count | Hardware emphasis |
|---------|---------------|--------------|-------------------|
| CPU-bound | — | ≈ physical cores | [[base clock speed]], SIMD |
| I/O-bound | Disk / NIC / peer | Can exceed cores | Queue depth, [[disk IOPS]], bandwidth |
| Mixed | Both | Measure | Avoid blind turbo spend |

I/O-bound services benefit from [[non-blocking]] loops or larger [[thread pool]]s so one blocked [[Thread]] does not stall all work — up to the point where [[context switching]] overhead dominates.

## Diagnosis

```bash
pidstat -d 1 -p PID    # disk read/write
pidstat -w 1           # context switches while "idle"
iostat -xz 1           # device utilization
```

If CPU is low but latency high, look downstream: storage, DNS, database, or [[Blocking]] on a shared mutex.

## Sources

- Google SRE Book — capacity planning
- Kerrisk, *The Linux Programming Interface*
- Wikipedia: [I/O bound](https://en.wikipedia.org/wiki/I/O_bound)
""")

note("critical sections.md", """
[[Operating System]] [[mutexes]] [[semaphores]] [[multi-threaded]] [[Thread]]

# Critical sections

> A critical section is a stretch of code that must not run concurrently with other threads touching the same data — mutual exclusion makes those regions safe.

Without protection, two threads updating a counter or linked list can interleave into torn state. **Locks** ([[mutexes]], spinlocks) or **lock-free atomics** serialize access.

```txt
Thread A: lock → read/modify/write shared → unlock
Thread B:        lock (waits) ───────────────► enters critical section
```

## Rules of thumb

- Keep critical sections **short** — no I/O or blocking calls inside if avoidable.
- One lock ordering across the codebase prevents deadlock.
- [[semaphores]] allow counting resources; mutexes are typically binary ownership.

Priority inversion happens when a low-priority thread holds a lock a high-priority thread needs — real-time kernels add priority inheritance.

## Sources

- Herlihy & Shavit, *The Art of Multiprocessor Programming*
- Silberschatz — synchronization chapter
- Wikipedia: [Critical section](https://en.wikipedia.org/wiki/Critical_section)
""")

note("Data Direction Register (DDR).md", """
[[Operating System]] [[bus]] [[Electronic Control Unit (ECU)]] [[analog interface]]

# Data Direction Register (DDR)

> On simple microcontrollers, a Data Direction Register sets each GPIO pin as input or output — the firmware-level switch that decides who drives the wire.

**GPIO** (General Purpose I/O) ports group pins. Writing a bit to the **DDR** (direction register) marks the corresponding data register bit as driven by the chip (**output**) or sampled from the pad (**input**). The name “DDR” here is **not** DRAM “Double Data Rate” memory.

```txt
DDR bit = 1 → output (MCU drives pin high/low)
DDR bit = 0 → input  (MCU reads external level)
```

## Operating system angle

Linux on embedded SoCs exposes GPIO through **libgpiod**, sysfs (legacy), or device tree pinctrl. User space rarely maps raw DDR addresses; the kernel’s GPIO subsystem abstracts port and pin numbers.

Contrast [[analog interface]] pins (ADC channels) and [[bus]] peripherals where direction is fixed by protocol (PCIe, I2C).

## Sources

- AVR / ARM Cortex-M vendor reference manuals — GPIO chapters
- Linux kernel documentation: [GPIO Subsystem](https://docs.kernel.org/driver-api/gpio/index.html)
- Wikipedia: [General-purpose input/output](https://en.wikipedia.org/wiki/General-purpose_input/output)
""")

note("discriptors.md", """
[[Operating System]] [[file descriptors]] [[handle]] [[system call]] [[Epoll]]

# Discriptors

> “Discriptors” in this vault refers to **descriptors** — kernel-managed integer handles (chiefly file descriptors) that stand for open objects: files, sockets, pipes, and epoll instances.

The spelling matches legacy notes; canonical term: **file descriptor** ([[file descriptors]]). On Unix, `open()`, `socket()`, and `accept()` return small integers; the process **descriptor table** maps them to `struct file` entries in the kernel.

## Descriptor table essentials

| Concept | Role |
|---------|------|
| fd number | Index user space passes to [[system call]] |
| `struct file` | Offset, flags, ops for one open instance |
| `dup()` / `fork()` | Share underlying file description |

Limits (`RLIMIT_NOFILE`, `fs.file-max`) cause `EMFILE` when leaked — common in long-running servers.

Windows uses opaque **handles** ([[handle]]) instead of small integers, but the abstraction role is the same.

## Multiplexing

[[Epoll]] (and `poll`, `select`) watches many descriptors for readiness — foundation of non-blocking servers ([[non-blocking]]).

## Sources

- Kerrisk, *The Linux Programming Interface* — file descriptors
- Linux `open(2)`, `fcntl(2)` manual pages
- Wikipedia: [File descriptor](https://en.wikipedia.org/wiki/File_descriptor)
""")

note("disk IOPS.md", """
[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[CPU IO Bound Task]] [[fsync]]

# disk IOPS

> IOPS (I/O operations per second) counts how many read/write commands a storage device completes per second — throughput in bytes and latency in milliseconds both matter for real workloads.

**IOPS** rises with smaller random IO on SSDs/NVMe; large sequential transfers measure **MB/s** instead. Controllers, queue depth, and block size all change the number.

## Rough reference (order of magnitude, not guarantees)

| Media | Random 4K IOPS (typical class) |
|-------|--------------------------------|
| HDD | tens to low hundreds |
| SATA SSD | tens of thousands |
| NVMe | hundreds of thousands+ |

## OS stack effects

The [[Buffer cache]] merges and delays writes — measured IOPS at the disk may be lower than application `write()` calls. [[fsync]] forces flush and can collapse IOPS under sync-heavy databases.

```bash
iostat -xz 1
fio --name=test --rw=randread --bs=4k --iodepth=32 --numjobs=1
```

[[CPU IO Bound Task]] services waiting on disk show low CPU and high `await` in `iostat`.

## Sources

- Brendan Gregg — storage performance methodology
- Wikipedia: [IOPS](https://en.wikipedia.org/wiki/IOPS)
- SNIA storage performance specifications
""")

note("Electronic Control Unit (ECU).md", """
[[Operating System]] [[analog interface]] [[Data Direction Register (DDR)]] [[bus]]

# Electronic Control Unit (ECU)

> An ECU is an embedded computer that reads sensors and drives actuators in real time — automotive engine control, ABS, or industrial controllers run a specialized OS (often RTOS) on bare metal or a thin POSIX layer.

Unlike a general-purpose PC booting [[Boot/UEFI]] and Linux desktop, an **ECU** typically:

- Runs **deterministic** control loops (milliseconds or microseconds).
- Uses [[analog interface]] and digital [[Data Direction Register (DDR)]] I/O directly.
- Communicates on CAN, LIN, or FlexRay rather than only [[PCI (Peripheral Component Interconnect)]].

## Software stack

```txt
Control algorithm → RTOS scheduler → drivers → MCU hardware
Optional: AUTOSAR, OBD diagnostics, secure boot
```

Resource limits mirror [[cgroup (Control Group)]] ideas but enforced statically at build time — fixed RAM, no swap ([[RAM and Swap memory]] rarely present).

## Sources

- Wikipedia: [Electronic control unit](https://en.wikipedia.org/wiki/Electronic_control_unit)
- AUTOSAR classic platform overview
- Barr Group — embedded systems architecture
""")

note("endian.md", """
[[Operating System]] [[TCP]] [[Linux/management/ELF (Editabl Linkable File)]] [[SYSV (System V)]]

# Endian

> Endianness defines which byte of a multi-byte integer sits at the lowest memory address — mismatches between CPU, wire protocol, and file format cause silent corruption unless converted.

**Little-endian:** least significant byte first (x86, x86-64, most ARM in practice). **Big-endian:** most significant byte first (many network protocols, some legacy CPUs).

## Where it appears

| Context | Convention |
|---------|------------|
| [[TCP]] / IP headers | Big-endian on the wire |
| [[ELF (Editabl Linkable File)]] | Header declares `EI_DATA` |
| User structs on disk | Must specify layout; `#pragma pack` pitfalls |

```c
uint32_t x = 0x01020304;
/* little-endian RAM: 04 03 02 01 */
```

Conversion: `htons`, `htonl`, `le32toh` / `be32toh` (BSD/glibc).

## Debugging

Hex dumps compared to protocol docs, wrong magic in binaries, checksum failures on network payloads — all classic endian bugs.

## Sources

- Stevens, *UNIX Network Programming* — byte ordering
- Wikipedia: [Endianness](https://en.wikipedia.org/wiki/Endianness)
- ELF specification — data encoding
""")

note("file descriptors.md", """
[[Operating System]] [[discriptors]] [[handle]] [[system call]] [[fsync]] [[Epoll]]

# File descriptors

> A file descriptor is a small non-negative integer the kernel gives your process to name an open file, socket, pipe, or device — every read, write, and mmap goes through it.

Returned by `open()`, `socket()`, `pipe()`, `epoll_create1()`, etc. The integer indexes the process **file descriptor table**; `dup2()` can remap stdin/stdout/stderr (0, 1, 2).

## Lifetime and sharing

- **`fork()`** — table copied; refcounts shared until close.
- **`exec()`** — descriptors marked close-on-exec (`FD_CLOEXEC`) close automatically.
- **Leaks** — forgotten sockets → `EMFILE`; use `lsof -p PID`.

## Flags that change behavior

| Flag | Effect |
|------|--------|
| `O_NONBLOCK` | [[non-blocking]] readiness ([[Epoll]]) |
| `O_APPEND` | Writes always at end |
| `O_DIRECT` | Bypass [[Buffer cache]] (alignment rules) |

Durability syscalls operate on fds: [[fsync]] on a file fd pushes dirty pages for that file.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux `open(2)`, `close(2)` manual pages
- Wikipedia: [File descriptor](https://en.wikipedia.org/wiki/File_descriptor)
""")

note("fsync.md", """
[[Operating System]] [[Buffer cache]] [[file descriptors]] [[system call]] [[Persistent Block Storage]]

# fsync

> fsync is the system call that pushes one file’s dirty cache data toward stable storage — the durability boundary databases rely on after a commit record is written.

`write()` success means data reached the [[Buffer cache]], not necessarily the NVMe platter or SSD flash. **`fsync(fd)`** (or `fdatasync` for data-only) schedules writeback for that file’s pages and waits for completion (modulo drive write cache policies).

## Related calls

| Call | Scope |
|------|--------|
| `fsync(fd)` | One file — data + needed metadata |
| `fdatasync(fd)` | Data only where possible |
| `sync()` | Global flush — heavy |

## Failure modes

- Drive **write cache** without capacitor — `fsync` returns success but data lost on power loss unless cache is disabled or battery-backed.
- Network filesystems — durability is only as strong as server guarantees.
- Containers — host crash still matters; [[Persistent Block Storage]] semantics pass through.

```bash
strace -e fsync -p PID
```

Pair with [[system call]] tracing and [[disk IOPS]] tuning for sync-heavy workloads.

## Sources

- Linux `fsync(2)` manual page
- PostgreSQL wiki — fsync and write reliability
- Wikipedia: [fsync](https://en.wikipedia.org/wiki/Syncing)
""")

note("handle.md", """
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
""")

note("Heap memory.md", """
[[Operating System]] [[RAM and Swap memory]] [[Browser memory]] [[OOM (Linux Out Of Memory)]] [[Stack Frame]]

# Heap memory

> Heap memory is dynamically allocated process memory — malloc, new, garbage-collected arenas — growing independently of the call stack and subject to fragmentation and OOM policy.

Contrast **stack** ([[Stack Frame]], [[stack pointer]]): automatic, LIFO, fixed per thread. **Heap** allocations persist until `free()` or GC; poor patterns cause leaks and fragmentation.

## Kernel interaction

Allocators (`malloc`, jemalloc, tcmalloc) request anonymous pages with `brk()` / `mmap()`. Resident size (RSS) counts toward [[cgroup (Control Group)]] and triggers [[OOM (Linux Out Of Memory)]] when over limit. Swap ([[RAM and Swap memory]]) may page cold heap pages to disk — disastrous for latency-sensitive JVM/Go heaps.

```bash
pmap -x PID
cat /proc/PID/smaps_rollup
```

## Browser and language runtimes

[[Browser memory]] splits JS heap versus native renderer allocations. Managed runtimes trade developer safety for GC pauses and larger footprint.

## Sources

- Wilson et al., “Dynamic Storage Allocation: A Survey and Classification”
- Kerrisk, *The Linux Programming Interface* — memory allocation
- Wikipedia: [Dynamic memory allocation](https://en.wikipedia.org/wiki/Dynamic_memory_allocation)
""")

note("How to manipulate memory directly.md", """
[[Operating System]] [[Heap memory]] [[shared memory]] [[assembly language]] [[file descriptors]]

# How to manipulate memory directly

> Direct memory manipulation means mapping bytes into your address space and touching them with pointers, atomics, or mmap — bypassing higher-level abstractions when you accept the safety cost.

## Common mechanisms (Linux)

| Mechanism | Use |
|-----------|-----|
| `mmap()` | Map file or anonymous memory |
| `/dev/mem`, `/dev/kmem` | Raw physical (root, dangerous) |
| [[shared memory]] (`shm_open`, `mmap`) | IPC between processes |
| `mlock()` | Pin pages — avoid swap |

```c
void *p = mmap(NULL, len, PROT_READ|PROT_WRITE,
               MAP_SHARED, fd, offset);
/* read/write *p — page faults populate from file or zero fill */
munmap(p, len);
```

## Safety and permissions

Modern kernels restrict raw hardware access. User space normally uses **file mappings** and **shared memory APIs**, not arbitrary physical addresses. Bugs become security vulnerabilities — use only with tests and capability boundaries.

For instruction-level access patterns see [[assembly language]] and [[opcode]] encoding.

## Sources

- Kerrisk, *The Linux Programming Interface* — `mmap`, shared memory
- Linux `mmap(2)`, `mlock(2)` manual pages
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective*
""")

note("interpreter.md", """
[[Operating System]] [[linker]] [[runtime]] [[Runtime Environment]] [[OS program]]

# Interpreter

> An interpreter executes source or bytecode instructions directly at runtime — trading startup simplicity and portability for lower peak speed compared with ahead-of-time compiled [[OS program]] binaries.

**Pure interpretation** fetches each instruction in a loop. **Bytecode VMs** (CPython, JVM without JIT, Ruby) decode opcodes ([[opcode]]) in software. **JIT** hybrids compile hot paths to machine code while retaining interpreter fallback.

## Versus compilation pipeline

```txt
Source → interpreter ──► run immediately

Source → compiler → object → [[linker]] → native binary → CPU
Source → compiler → bytecode → VM interpreter / JIT
```

## OS involvement

The interpreter itself is a native executable loaded by the loader ([[Boot/UEFI]] chain → kernel → execve). It makes [[system call]]s on behalf of scripts — same [[file descriptors]] and [[Heap memory]] rules.

Shebang `#!/usr/bin/env python3` selects the interpreter binary via `execve`.

## Sources

- Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools*
- Wikipedia: [Interpreter (computing)](https://en.wikipedia.org/wiki/Interpreter_(computing))
""")

note("Inter Process Communication.md", """
[[Operating System]] [[process]] [[shared memory]] [[file descriptors]] [[Thread]] [[IPC namespace]]

# Inter Process Communication

> Inter-process communication (IPC) lets separate address spaces exchange data and synchronize — pipes, sockets, shared memory, and message queues are the usual Unix toolkit.

Each [[process]] has private virtual memory. **IPC** bridges isolation:

| Mechanism | Copy behavior | Typical use |
|-----------|---------------|-------------|
| Pipe / socket | Kernel copies bytes | CLI tools, services |
| [[shared memory]] | Mapped into both | High bandwidth |
| Unix domain socket | Local, fd-based | DB clients on same host |
| Signals | Minimal metadata | Events, job control |

## Namespaces

[[IPC namespace]] isolates System V IPC identifiers and POSIX mqueue names — containers see their own IPC universe.

Threads in one process ([[Thread]]) share memory by default — use [[mutexes]] instead of IPC.

## Sources

- Stevens, *Advanced Programming in the UNIX Environment* — IPC chapters
- Linux `pipe(7)`, `unix(7)`, `shm_overview(7)` manual pages
- Wikipedia: [Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication)
""")

note("IPC namespace.md", """
[[Operating System]] [[Inter Process Communication]] [[UTS namespace]] [[cgroup (Control Group)]] [[process]]

# IPC namespace

> The IPC namespace isolates System V semaphores, message queues, and shared memory identifiers — and POSIX message queue names — so containers cannot collide on key `12345`.

Created with `clone(CLONE_NEWIPC)` or `unshare -i`. Processes in different IPC namespaces see disjoint IPC object IDs even if numeric keys match.

## Related isolation

Linux namespaces stack:

- [[UTS namespace]] — hostname
- PID, mount, network, user namespaces
- [[cgroup (Control Group)]] — resource limits (not a namespace but paired)

```bash
unshare -i bash
ipcs   # view SysV objects in current namespace
```

## Sources

- Linux `ipc_namespaces(7)` manual page
- Linux `namespaces(7)` overview
- Wikipedia: [Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)
""")

note("kernel ring buffer.md", """
[[Operating System]] [[atomic ring buffer]] [[Rolling Buffer]] [[kernel subsystem]] [[right buffer]]

# Kernel ring buffer

> The kernel ring buffer is the fixed-size circular log where printk records land — what you read with dmesg before structured logging took over in many setups.

Implemented as a lock-protected or atomic [[atomic ring buffer]] of text records. Drivers and subsystems call `printk()` at various log levels; userspace reads `/dev/kmsg` or runs `dmesg`.

## Behavior under load

- **Overflow** — oldest messages may drop with “lost N messages” notice.
- **Rate limiting** — `printk_ratelimited` prevents floods.
- **Persistent journal** — systemd-journald also captures userspace; kernel buffer still bootstraps early boot before root mount.

```bash
dmesg -T -w
dmesg --level=err,warn
```

Contrast [[Rolling Buffer]] in application logging and [[right buffer]] sizing for latency-sensitive capture.

## Sources

- Linux kernel documentation: [Printk](https://docs.kernel.org/core-api/printk-basics.html)
- Linux `dmesg(1)` manual page
- Wikipedia: [Kernel log](https://en.wikipedia.org/wiki/Kernel_log)
""")

note("kernel subsystem.md", """
[[Operating System]] [[system call]] [[Buffer cache]] [[context switching]] [[kernel ring buffer]]

# Kernel subsystem

> A kernel subsystem is a major functional area inside monolithic kernels like Linux — scheduler, memory management, VFS, networking, block layer — sharing address space but modular boundaries.

Linux organizes work into subsystems with clear APIs:

| Subsystem | Responsibility |
|-----------|------------------|
| Scheduler | [[Thread]] placement, [[context switching]] |
| MM | Pages, [[Heap memory]] backing, [[Buffer cache]] |
| VFS | Paths, inodes, [[file descriptors]] |
| Block layer | Queues to [[Persistent Block Storage]] |
| Net stack | Sockets, protocols |

Loadable **kernel modules** extend subsystems without full rebuild. eBPF programs attach to hooks in networking and tracing.

User entry is almost always [[system call]]; diagnostics use `procfs`, `sysfs`, `tracepoints`, and [[kernel ring buffer]] messages.

## Sources

- Robert Love, *Linux Kernel Development*
- Linux kernel documentation: [Core API](https://docs.kernel.org/core-api/index.html)
- Wikipedia: [Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel)
""")

note("linker.md", """
[[Operating System]] [[interpreter]] [[OS program]] [[opcode]] [[Linux/management/ELF (Editabl Linkable File)]]

# Linker

> The linker combines compiled object files and libraries into one executable or shared object — resolving symbols, assigning final addresses, and producing the ELF binary the kernel execve loads.

After the compiler emits `.o` files with unresolved references, **`ld`** (or `gold`, `lld`):

1. Merges `.text`, `.data`, `.bss` sections.
2. Resolves `malloc`, `main`, etc. against libc.
3. Applies relocations for PIC/PIE.
4. Outputs ELF ([[Linux/management/ELF (Editabl Linkable File)]]) or static binary.

```txt
main.c → cc -c → main.o ─┐
libc.so ─────────────────┼→ ld → a.out (ELF)
other.o ─────────────────┘
```

Dynamic linking defers some symbols to runtime **loader** (`ld.so`) — part of the [[Runtime Environment]].

Contrast [[interpreter]] execution of scripts without a separate link step for user code.

## Sources

- Levine, *Linkers and Loaders*
- Linux `ld(1)`, ELF specification
- Wikipedia: [Linker (computing)](https://en.wikipedia.org/wiki/Linker_(computing))
""")

note("logical partitions.md", """
[[Operating System]] [[MBR]] [[Persistent Block Storage]] [[cgroup (Control Group)]]

# Logical partitions

> Logical partitions extend MBR’s four primary slot limit by nesting partitions inside an extended container — a legacy layout largely replaced by GPT on UEFI systems.

**MBR** allows four **primary** partition entries. One can be an **extended** partition holding many **logical** partitions chained in linked EBRs. Tools (`fdisk`, `parted`) expose them as `/dev/sda5`, `/dev/sda6`, …

## Limits and modern alternative

- Complexity and fragility of EBR chains.
- 2 TiB disk size cap on MBR layout.
- **GPT** on [[Boot/UEFI]] machines supports dozens of primary partitions without extended/logical gymnastics.

Conceptually similar to dividing a machine into resource slices ([[cgroup (Control Group)]]) — different problem domain, same “partition the namespace” idea.

## Sources

- Wikipedia: [Extended boot record](https://en.wikipedia.org/wiki/Extended_boot_record), [GUID Partition Table](https://en.wikipedia.org/wiki/GUID_Partition_Table)
- Microsoft documentation — disk partitioning
""")

note("MBR.md", """
[[Operating System]] [[MBR(Master Boot Record)]] [[Boot/UEFI]] [[logical partitions]] [[Persistent Block Storage]]

# MBR

> The Master Boot Record is the first 512-byte sector of a legacy BIOS-boot disk — partition table plus a tiny boot code stub that chain-loads the real bootloader.

**MBR** layout (classic):

```txt
Byte 0–445:   boot code (446 bytes max)
Byte 446–510: 4 × 16-byte partition entries
Byte 510–511: 0xAA55 signature
```

One partition may be marked **active** for BIOS handoff. Extended partitions enable [[logical partitions]] beyond four slots.

## Modern status

[[Boot/UEFI]] + GPT replaced MBR for new systems (>2 TiB disks, Secure Boot). MBR remains in CSM legacy mode and old images.

Boot repair on MBR disks: reinstall stage1/stage2 to the boot sector or embed GRUB in the gap after MBR.

## Sources

- Wikipedia: [Master boot record](https://en.wikipedia.org/wiki/Master_boot_record)
- GRUB documentation — BIOS boot installation
""")

note("MBR(Master Boot Record).md", """
[[Operating System]] [[MBR]] [[Boot/UEFI]] [[Persistent Block Storage]]

# MBR(Master Boot Record)

> This note aliases the Master Boot Record — the first-sector BIOS boot structure with partition table and 446-byte code field; see [[MBR]] for full detail.

The **Master Boot Record** is not a file — it is LBA 0 on a disk. Corrupt partition entries or overwritten boot code produce “Operating system not found” on legacy firmware paths.

Key facts:

- 512-byte sector, signature **0xAA55** at end.
- Four primary partitions; extended type for [[logical partitions]].
- Boot code too small for modern features — only enough to jump to volume boot record or GRUB stage2.

UEFI systems may still contain an MBR-style protective or hybrid layout on GPT disks when **CSM** is enabled ([[Boot/UEFI (2)]]).

Canonical detail: [[MBR]].

## Sources

- Wikipedia: [Master boot record](https://en.wikipedia.org/wiki/Master_boot_record)
- UEFI specification — legacy BIOS compatibility
""")

note("multiple levels of buffering.md", """
[[Operating System]] [[buffer]] [[buffer lifecycle]] [[Buffer cache]] [[Blocking]]

# Multiple levels of buffering

> Real systems stack buffers at every speed boundary — application, libc, socket, kernel page cache, disk controller — and flushing one layer does not flush the layers below.

Each [[buffer]] exists because the producer and consumer run at different rates or granularities. **Multiple levels** improve throughput but add **latency** and **durability gaps**.

```txt
App buffer → stdio → socket SNDBUF → TCP → NIC ring → switch → disk cache → NAND
```

## Common mistakes

| Action | What it does *not* do |
|--------|------------------------|
| `fflush(stdout)` | [[fsync]] file on disk |
| `socket write()` return | Peer application read |
| `close()` | Guarantee persistence |

Tuning only the largest buffer hides backpressure until something smaller fills and blocks ([[Blocking]]).

See [[buffer lifecycle]] for state transitions at one layer.

## Sources

- Stevens, *UNIX Network Programming*
- Tanenbaum, *Modern Operating Systems* — I/O buffering
""")

note("multi-threaded.md", """
[[Operating System]] [[Single-threaded]] [[Thread]] [[thread pool]] [[mutexes]] [[context switching]]

# Multi-threaded

> A multi-threaded program runs several threads of control in one process sharing address space and file descriptors — parallelism without separate [[Inter Process Communication]] for every byte.

Each [[Thread]] has its own stack ([[Stack Frame]]) but shares [[Heap memory]] and open [[file descriptors]]. The kernel schedules threads independently → [[context switching]].

## When multi-threading helps

- Parallel CPU work on multiple cores ([[Single Instruction, Multiple Data (SIMD)]] is orthogonal — data parallelism inside one thread).
- [[CPU IO Bound Task]] workloads — one thread blocks on I/O while others run.
- Structured servers using [[thread pool]].

## Costs

- [[critical sections]] and [[mutexes]] — contention serializes work.
- Harder debugging — [[Stack trace]] per thread, races, deadlocks.

Versus [[Single-threaded]] event loops: fewer locks, must use [[non-blocking]] I/O for concurrency.

## Sources

- Herlihy & Shavit, *The Art of Multiprocessor Programming*
- Silberschatz — threads chapter
- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
""")

note("mutexes.md", """
[[Operating System]] [[critical sections]] [[semaphores]] [[Thread]] [[context switching]]

# Mutexes

> A mutex (mutual exclusion lock) ensures at most one thread runs a protected [[critical sections]] region at a time — the default tool when shared mutable state must not race.

POSIX **`pthread_mutex_t`**, C++ `std::mutex`, Java `synchronized` — all map to kernel **futex** waits when contended: fast atomic try in user space, [[Blocking]] sleep if held.

## Practices

- Lock ordering prevents deadlock (always A then B).
- Hold locks briefly — no disk I/O inside if possible.
- Prefer higher-level message passing when ownership is unclear.

[[semaphores]] generalize to counting resources; mutexes are typically binary.

Heavy contention increases [[context switching]] and cache line bouncing between cores.

## Sources

- Kerrisk, *The Linux Programming Interface* — mutexes and futex
- Wikipedia: [Mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion)
""")

note("non-blocking.md", """
[[Operating System]] [[Blocking]] [[Blocking Vs Non-Blocking]] [[Epoll]] [[system call]]

# Non-blocking

> Non-blocking I/O returns immediately when data is not ready — the caller must retry or wait via an event multiplexer instead of sleeping inside the kernel.

Set with `fcntl(O_NONBLOCK)` on [[file descriptors]]. `read()` / `write()` / `accept()` fail with **`EAGAIN`** or **`EWOULDBLOCK`** until the fd is ready.

## Event-driven pattern

```txt
epoll_wait(fds ready) → read/write each ready fd → repeat
```

Pairs with [[Epoll]], `kqueue`, or `io_uring` for many connections and few [[Thread]]s.

Contrast [[Blocking]] simplicity — choose using [[Blocking Vs Non-Blocking]] criteria.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux `fcntl(2)`, `epoll(7)` manual pages
""")

note("one-level storage system.md", """
[[Operating System]] [[abstract storage location]] [[Persistent Block Storage]] [[Buffer cache]]

# One-level storage system

> A one-level storage system presents a single uniform address space for programs and persistent data — the classic vision where memory and disk are indistinguishable to the programmer.

Historically associated with **Multics** and early MIT/Flex machine research: no explicit separate “file read” versus “load instruction” — paging and segmentation hide media. Modern systems approximate pieces of this:

- **Memory-mapped files** — file bytes appear as virtual addresses.
- **Unified page cache** ([[Buffer cache]]) — same pages back file I/O and mmap.
- **NVMe + large RAM** — fast swap and cache blur latency gaps.

Full transparency fails on **durability** and **capacity** — RAM remains volatile without flush ([[fsync]]), and cost per byte still differs.

## Sources

- Corbato et al., Multics papers — one-level store concept
- Denning, “Virtual Memory” — ACM Computing Surveys
- Wikipedia: [Single-level store](https://en.wikipedia.org/wiki/Single-level_store)
""")

note("opcode.md", """
[[Operating System]] [[assembly language]] [[interpreter]] [[Stack based programming language]]

# Opcode

> An opcode is the numeric operation code in a machine or bytecode instruction — the CPU or VM decoder reads it and dispatches the right micro-operation.

In **machine code**, opcodes sit in executable `.text` sections ([[linker]] output). In **bytecode VMs**, opcodes index an interpreter loop ([[interpreter]]) or JIT tables.

Example (conceptual x86): `0x0F 0x05` → `syscall` for [[system call]] entry.

## Stack machines

Some ISAs and bytecodes ([[Stack based programming language]]) use opcodes that push/pop an operand stack instead of naming registers — JVM, Forth, some embedded VMs.

Security: unexpected opcodes in data → crash or exploit if execution jumps into data.

## Sources

- Intel/AMD ISA manuals — instruction encodings
- Wikipedia: [Opcode](https://en.wikipedia.org/wiki/Opcode)
""")

note("OS program.md", """
[[Operating System]] [[linker]] [[interpreter]] [[system call]] [[Runtime Environment]] [[process]]

# OS program

> An OS program is an executable image the kernel loads into a [[process]] — ELF binary, script with shebang, or dynamic shared object run by the loader.

Lifecycle:

```txt
User invokes path → execve() → kernel reads ELF headers
→ maps segments → sets up stack/heap → start (e.g. _start → main)
→ program runs via [[system call]] until exit
```

Formats: ELF on Linux ([[Linux/management/ELF (Editabl Linkable File)]]), PE on Windows. Scripts delegate to [[interpreter]] binaries.

The **runtime** ([[runtime]], [[Runtime Environment]]) supplies libc, thread startup, and dynamic linking after the kernel hands off control.

## Sources

- Bryant & O’Hallaron, *Computer Systems*
- Linux `execve(2)`, ELF specification
- Wikipedia: [Executable](https://en.wikipedia.org/wiki/Executable)
""")

note("PCI (Peripheral Component Interconnect).md", """
[[Operating System]] [[bus]] [[system bus]] [[Boot/UEFI]] [[Persistent Block Storage]]

# PCI (Peripheral Component Interconnect)

> PCI and its successor PCIe are standard local buses for attaching NICs, GPUs, NVMe controllers, and chipset devices — enumerated at boot with vendor/device IDs and BAR memory regions.

**PCIe** (Express) serial lanes replace parallel PCI but retain the **PCI** configuration model. Firmware ([[Boot/UEFI]]) and the kernel walk the **PCIe tree**, assign resources, and bind **drivers**.

```bash
lspci -nn
lspci -vv -s 01:00.0
```

## OS view

- **MMIO** — driver maps BAR into kernel space.
- **DMA** — devices transfer to RAM ([[Buffer cache]] pages).
- **MSI/MSI-X** — interrupts for completion events.

Hot-plug (some servers), ACS, and IOMMU (VT-d) affect virtualization passthrough.

Parent topic: [[bus]], [[system bus]].

## Sources

- PCI-SIG PCIe base specification
- Linux kernel documentation: [PCI Subsystem](https://docs.kernel.org/PCI/index.html)
- Wikipedia: [PCI Express](https://en.wikipedia.org/wiki/PCI_Express)
""")

note("Persistent Block Storage.md", """
[[Operating System]] [[abstract storage location]] [[disk IOPS]] [[Buffer cache]] [[fsync]] [[MBR]]

# Persistent Block Storage

> Persistent block storage survives power-off — HDDs, SSDs, NVMe, SAN LUNs — exposed to the OS as numbered sectors or volumes layered with partition tables and file systems.

The block interface reads/writes fixed **sectors** (often 512 B or 4 KiB logical). File systems map paths to block ranges; the [[Buffer cache]] caches those blocks in RAM.

## Layout stack

```txt
Application path → VFS → filesystem → block layer → driver → NVMe/SATA
Partition: [[MBR]] or GPT ([[Boot/UEFI]]) → [[logical partitions]]
```

## Durability chain

Writes may sit in drive **write cache** until [[fsync]] and flush commands complete — critical for databases. [[disk IOPS]] and queue depth define throughput under load.

Cloud volumes (EBS, Persistent Disk) are remote block devices with their own latency and durability SLAs.

## Sources

- Linux kernel documentation: [Block layer](https://docs.kernel.org/block/index.html)
- SNIA storage tutorials
- Wikipedia: [Block (data storage)](https://en.wikipedia.org/wiki/Block_(data_storage))
""")

note("RAM and Swap memory.md", """
[[Operating System]] [[Heap memory]] [[Buffer cache]] [[OOM (Linux Out Of Memory)]] [[cgroup (Control Group)]]

# RAM and Swap memory

> RAM holds running code, stacks, heaps, and cache; swap extends virtual memory to disk when physical pages are scarce — trading latency for capacity.

Linux uses **anonymous** pages (heap, stack) and **file-backed** pages ([[Buffer cache]]). Under pressure the **swap** subsystem pages cold anonymous memory to a swap file or partition, freeing RAM.

```bash
free -h
swapon --show
cat /proc/swaps
```

## Behavior

- High swap use → latency spikes on page faults ([[CPU IO Bound Task]]).
- `vm.swappiness` biases reclaim toward cache versus process pages.
- [[cgroup (Control Group)]] `memory.max` can OOM-kill before swap helps.

Swap is not a durability mechanism — powered-off swap does not preserve intentional persistence ([[fsync]] matters for files).

## Sources

- Linux kernel documentation: [Swap Management](https://docs.kernel.org/admin-guide/mm/concepts.html)
- Linux `swapon(8)` manual page
- Wikipedia: [Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)
""")

note("right buffer.md", """
[[Operating System]] [[buffer]] [[Rolling Buffer]] [[kernel ring buffer]] [[atomic ring buffer]]

# Right buffer

> Choosing the right buffer size balances latency, memory, and drop behavior — too small causes syscalls or overruns; too large hides backpressure until memory pressure hits.

No universal constant: audio streams want low latency (small ring), bulk export wants large TCP windows, kernel logs use fixed [[kernel ring buffer]] capacity.

## Sizing questions

| Question | If wrong |
|----------|----------|
| Producer burst rate? | Overrun in [[atomic ring buffer]] |
| Consumer steady drain? | [[Blocking]] producer |
| Memory budget per connection? | OOM under fan-in |
| Durability need? | Large RAM buffer loses data on crash |

Tune with measurement: `strace` syscall counts, drop counters, `perf`.

Related patterns: [[Rolling Buffer]], [[multiple levels of buffering]].

## Sources

- Stevens, *UNIX Network Programming* — socket buffer tuning
- Linux `socket(7)` — SO_SNDBUF, SO_RCVBUF
""")

note("Rolling Buffer.md", """
[[Operating System]] [[atomic ring buffer]] [[kernel ring buffer]] [[right buffer]] [[buffer]]

# Rolling Buffer

> A rolling buffer overwrites the oldest entries when full — fixed memory for logs, metrics, and telemetry where history beyond N samples is expendable.

Unlike a blocking queue that stops producers, a **rolling** (circular) design keeps the most recent window. Implementation matches [[atomic ring buffer]] mechanics with policy: drop-on-full versus block-on-full.

## Uses

- Application log tail in memory
- Metrics dashboards (last 15 minutes)
- Kernel printk before journald ([[kernel ring buffer]])

Choose [[right buffer]] capacity from acceptable loss horizon — “if I only keep 1 MB of logs, what incidents become unexplainable?”

## Sources

- Wikipedia: [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer)
- Linux kernel ring buffer design discussions (LKML)
""")

note("Runtime Environment.md", """
[[Operating System]] [[runtime]] [[interpreter]] [[linker]] [[OS program]]

# Runtime Environment

> The runtime environment is everything that executes your program after the kernel starts it — dynamic linker, libc, thread library, GC, and language builtins.

For a C binary: kernel `execve` → **ld.so** maps libc and resolves symbols → `_start` → `main`. For JVM: native `java` stub loads bytecode, JIT, and standard library.

## Components

| Piece | Role |
|-------|------|
| Dynamic linker | Loads `.so`, relocates ([[linker]] at load time) |
| libc | [[system call]] wrappers, malloc |
| Language runtime | Exceptions, GC, goroutine scheduler |
| [[interpreter]] | Executes non-native code paths |

Container images ship a minimal runtime (musl vs glibc) — ABI mismatch breaks binaries.

See [[runtime]] for shorter cross-reference.

## Sources

- Levine, *Linkers and Loaders*
- Linux `ld.so(8)`, `ldd(1)` manual pages
""")

note("runtime.md", """
[[Operating System]] [[Runtime Environment]] [[interpreter]] [[OS program]] [[Heap memory]]

# Runtime

> Runtime is the active phase when a program executes — and colloquially the libraries and services that phase depends on, distinct from compile/link time.

**Compile time:** source → objects ([[linker]]). **Runtime:** CPU executes instructions, allocator serves [[Heap memory]], I/O uses [[file descriptors]].

Managed languages add bytecode execution ([[interpreter]]), JIT compilation, and garbage collection inside the [[Runtime Environment]].

Debugging “runtime error” versus “compile error” separates logic after launch from syntax and type failures before launch.

## Sources

- Wikipedia: [Runtime system](https://en.wikipedia.org/wiki/Runtime_system)
- Bryant & O’Hallaron, *Computer Systems*
""")

note("semaphores.md", """
[[Operating System]] [[mutexes]] [[critical sections]] [[Thread]] [[Inter Process Communication]]

# Semaphores

> A semaphore counts permits — threads wait when the count is zero and post when releasing a resource — generalizing [[mutexes]] from binary locks to N-way pools.

**POSIX semaphores** (`sem_wait`, `sem_post`) and **System V semaphores** (in [[IPC namespace]]) coordinate producers and consumers, connection pools, and [[critical sections]] with bounded occupancy.

```txt
count = 3 → three threads may enter; fourth blocks until post
```

Binary semaphore ≈ mutex (with different ownership semantics). Counting semaphore models empty/full slots in bounded buffers.

## Sources

- Dijkstra — semaphore original definition
- Kerrisk, *The Linux Programming Interface*
- Wikipedia: [Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming))
""")

note("shared memory.md", """
[[Operating System]] [[Inter Process Communication]] [[How to manipulate memory directly]] [[mutexes]] [[file descriptors]]

# Shared memory

> Shared memory maps the same physical pages into multiple processes — zero-copy IPC once mapped, requiring separate synchronization for concurrent access.

POSIX: `shm_open` + `mmap`. System V: `shmget`, `shmat`. After mapping, reads/writes are plain loads/stores — use [[mutexes]] or atomics in the shared region.

```txt
Process A ──┐
            ├── same page frames → fast bulk data
Process B ──┘
```

Contrast pipes (kernel copies each byte). [[IPC namespace]] isolates SysV keys between containers.

## Sources

- Stevens, *Advanced Programming in the UNIX Environment*
- Linux `shm_overview(7)` manual page
- Wikipedia: [Shared memory](https://en.wikipedia.org/wiki/Shared_memory)
""")

note("Single Instruction, Multiple Data (SIMD).md", """
[[Operating System]] [[base clock speed]] [[multi-threaded]] [[Thread]]

# Single Instruction, Multiple Data (SIMD)

> SIMD executes one instruction across a vector of data lanes — SSE, AVX, AVX-512 on x86, NEON on ARM — speeding numeric kernels without extra [[Thread]]s.

The CPU applies the same opcode ([[opcode]]) to multiple operands in parallel registers. Compilers auto-vectorize loops; intrinsics (`__m256`) hand-tune hot paths.

## Versus threading

| Approach | Parallelism type |
|----------|------------------|
| SIMD | Data parallel in one thread |
| [[multi-threaded]] | Multiple threads on cores |

Use SIMD for dense math; use threads for independent tasks or I/O overlap ([[CPU IO Bound Task]]).

Check CPU flags: `grep avx /proc/cpuinfo`, `lscpu`.

## Sources

- Intel Intrinsics Guide
- Hennessy & Patterson — SIMD chapters
- Wikipedia: [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data)
""")

note("Single-threaded.md", """
[[Operating System]] [[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking]]

# Single-threaded

> A single-threaded program has one call stack and one scheduler entity — concurrency must come from non-blocking I/O, events, or external processes, not sibling threads.

Examples: early Node.js event loop, Redis main thread (with helper I/O threads in newer versions), many embedded firmware loops.

## Advantages

- No [[mutexes]] on shared in-process state.
- Easier reasoning about [[Stack Frame]] and globals.
- Lower [[context switching]] than oversized thread pools.

## Limits

- One CPU-bound loop blocks everything — offload CPU work or use [[multi-threaded]] workers.
- Must use [[non-blocking]] / [[Epoll]] for many network clients.

## Sources

- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
- Node.js documentation — event loop model
""")

note("SMT threads.md", """
[[Operating System]] [[Thread]] [[context switching]] [[base clock speed]] [[TDP]]

# SMT threads

> Simultaneous multithreading (Intel Hyper-Threading, AMD SMT) exposes two logical CPUs per physical core — sharing execution units while each has its own architectural state.

The OS schedules [[Thread]]s on **logical processors**; two runnable threads on sibling hyperthreads compete for the same core’s ALUs and caches.

## Implications

- CPU-bound pairs on one core rarely yield 2× throughput — often ~1.2–1.3× depending on workload.
- [[context switching]] between siblings is cheaper than cross-core but still contends.
- Pin latency-sensitive threads to exclusive cores when [[TDP]] and licensing allow.

```bash
lscpu | grep -E 'Thread|Core|Socket'
cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list
```

## Sources

- Intel 64 Architecture optimization manual — Hyper-Threading
- Wikipedia: [Simultaneous multithreading](https://en.wikipedia.org/wiki/Simultaneous_multithreading)
""")

note("Stack based programming language.md", """
[[Operating System]] [[opcode]] [[Stack Frame]] [[stack pointer]] [[interpreter]]

# Stack based programming language

> Stack-based languages express programs as sequences of operations on an operand stack — no named registers in the source model; the JVM, Forth, and RPN calculators work this way.

Each [[opcode]] pushes or pops values:

```txt
push 2 → push 3 → add → stack top is 5
```

The **hardware** still uses registers under JIT/AOT compilation, but the language semantics are stack-oriented.

## OS/runtime link

Bytecode [[interpreter]] loops manipulate a virtual stack in [[Heap memory]]; native JIT maps hot traces to machine code. Deep stacks overflow with `StackOverflowError` — separate from kernel stack limits ([[Stack Frame]]).

Contrast register-machine ISAs targeted by [[assembly language]].

## Sources

- JVM specification — operand stack
- Wikipedia: [Stack machine](https://en.wikipedia.org/wiki/Stack_machine)
""")

note("Stack Frame.md", """
[[Operating System]] [[stack pointer]] [[Stack trace]] [[Thread]] [[Heap memory]]

# Stack Frame

> A stack frame is the block of memory a function call pushes — return address, saved registers, locals — nested in LIFO order on the thread stack.

Call sequence:

```txt
main frame → foo frame → bar frame
              ↑ stack pointer moves down on call, up on return
```

Each [[Thread]] has a fixed or growable stack region; overflow causes segmentation fault — not to be confused with [[Heap memory]] exhaustion.

Debuggers unwind frames to print [[Stack trace]] after crashes.

## Sources

- Bryant & O’Hallaron, *Computer Systems* — procedure call convention
- Wikipedia: [Call stack](https://en.wikipedia.org/wiki/Call_stack)
""")

note("stack pointer.md", """
[[Operating System]] [[Stack Frame]] [[Stack trace]] [[assembly language]]

# Stack pointer

> The stack pointer register (RSP on x86-64, SP on ARM) tracks the top of the current thread stack — decremented on call, incremented on return.

Must stay **aligned** per ABI (often 16-byte on x86-64). Corruption — buffer overflow past a local array — overwrites return address → arbitrary code or crash in [[Stack trace]].

Low-level debugging and [[assembly language]] show explicit `push`/`pop` or `sub rsp` prologues establishing a [[Stack Frame]].

## Sources

- System V AMD64 ABI — stack alignment
- Intel SDM — stack pointer semantics
""")

note("Stack trace.md", """
[[Operating System]] [[Stack Frame]] [[stack pointer]] [[process]] [[gdb]]

# Stack trace

> A stack trace lists the chain of function calls at a point in time — the first map when a program crashes, deadlocks, or logs an exception.

Generated by walking linked [[Stack Frame]]s using frame pointers or unwind tables (.eh_frame). Tools: `gdb bt`, language stack dumps, `pstack`.

```txt
#0  crash() at bug.c:12
#1  handle() at srv.c:88
#2  main() at srv.c:40
```

Symbol resolution needs debug symbols (-g) or separate debuginfo packages.

Kernel oops traces differ — kernel stack, not user [[process]] stack.

## Sources

- Kerrisk, *The Linux Programming Interface* — core dumps
- Linux `backtrace(3)`, `gdb(1)` manual pages
- Wikipedia: [Stack trace](https://en.wikipedia.org/wiki/Stack_trace)
""")

note("system call.md", """
[[Operating System]] [[file descriptors]] [[fsync]] [[process]] [[Epoll]] [[handle]]

# System call

> A system call is the controlled gateway from user mode into the kernel — open files, map memory, spawn processes, send packets — with privilege checks on every entry.

User code cannot touch device registers directly. It places the **syscall number** and arguments in registers, executes `syscall` (x86-64) or `svc` (ARM), and traps to the kernel handler table.

```txt
write(fd, buf, n) → libc stub → syscall → sys_write → VFS/block/net
```

Returns success value or `-1` with `errno`. Blocking syscalls sleep the [[Thread]] ([[Blocking]]); non-blocking return `EAGAIN` ([[non-blocking]]).

Tracing: `strace -p PID`; production: eBPF ([[Linux/eBPF]]).

Durability example: [[fsync]] after [[Buffer cache]] writes.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux syscall(2), individual syscall pages on man7.org
- Wikipedia: [System call](https://en.wikipedia.org/wiki/System_call)
""")

note("Take snapshot.md", """
[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[fsync]]

# Take snapshot

> A storage snapshot is a point-in-time view of a volume — copy-on-write or redirect-on-write — letting you roll back or clone without copying every block upfront.

File systems (Btrfs, ZFS), LVM, cloud volume APIs, and VM hypervisors expose **snapshot** operations distinct from normal file copy.

## Consistency

Application-consistent snapshots quiesce writers or flush journals ([[fsync]]). Crash-consistent snapshots capture disk mid-write — databases may need recovery.

```txt
Live volume → snapshot COW → mount clone for backup/forensics
```

Snapshots are not backups until replicated off-box; they share pool with source on failure.

Related: [[Persistent Block Storage]], [[RAM and Swap memory]] (memory snapshots in VMs — different mechanism).

## Sources

- Wikipedia: [Snapshot (computer storage)](https://en.wikipedia.org/wiki/Snapshot_(computer_storage))
- LVM2 documentation — snap shots
- AWS EBS snapshot documentation
""")

note("TDP.md", """
[[Operating System]] [[base clock speed]] [[SMT threads]] [[cgroup (Control Group)]]

# TDP

> TDP (Thermal Design Power) is the heat a cooling solution must dissipate at sustained load — not peak power, but the thermal envelope that governs throttling and [[base clock speed]].

CPU vendors specify TDP in watts; actual power varies with workload, turbo, and [[SMT threads]] utilization. Exceed thermal limits → **throttling** → lower frequency and higher latency.

Datacenter planning pairs TDP with rack power and [[cgroup (Control Group)]]-limited workloads in shared hosts.

```bash
turbostat --Summary --quiet
cat /sys/class/thermal/thermal_zone*/temp
```

## Sources

- Intel product specification — TDP definition
- Wikipedia: [Thermal design power](https://en.wikipedia.org/wiki/Thermal_design_power)
""")

note("Thread.md", """
[[Operating System]] [[multi-threaded]] [[Single-threaded]] [[context switching]] [[mutexes]] [[process]]

# Thread

> A thread is the unit of CPU scheduling inside a [[process]] — own stack and registers, shared address space and file descriptors with siblings.

Created with `pthread_create`, `clone`, or language threads (Java, Go goroutines mapped to OS threads). The kernel scheduler assigns threads to cores → [[context switching]] when blocked or preempted.

Synchronize shared mutable state with [[mutexes]], [[semaphores]], or atomics — otherwise data races corrupt [[Heap memory]] structures.

## Sources

- Silberschatz — threads and concurrency
- Linux `pthread(7)`, `clone(2)` manual pages
- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
""")

note("thread pool.md", """
[[Operating System]] [[multi-threaded]] [[Thread]] [[CPU IO Bound Task]] [[context switching]] [[thread-safe queue]]

# Thread pool

> A thread pool keeps a fixed set of worker threads pulling tasks from a queue — amortizing thread creation cost and bounding concurrency versus unbounded `pthread_create`.

Pattern:

```txt
Submit task → queue ([[thread-safe queue]]) → idle worker runs → repeat
```

Size for **CPU-bound** work ≈ core count; **I/O-bound** ([[CPU IO Bound Task]]) may use more workers but watch [[context switching]] and lock contention ([[mutexes]]).

Used in Java `ExecutorService`, Go worker pools, nginx optional thread module.

## Sources

- Java Concurrency in Practice — thread pool sizing
- Wikipedia: [Thread pool](https://en.wikipedia.org/wiki/Thread_pool)
""")

note("thread-safe queue.md", """
[[Operating System]] [[thread pool]] [[multi-threaded]] [[mutexes]] [[atomic ring buffer]]

# Thread-safe queue

> A thread-safe queue lets multiple producers and consumers enqueue and dequeue without corrupting linked structure — locks, condition variables, or lock-free rings inside.

Backs [[thread pool]] task dispatch, logging pipelines, and bounded work buffers. Implementation choices:

| Style | Trade-off |
|-------|-----------|
| Mutex + condvar | Simple, contended under load |
| [[atomic ring buffer]] | Fast SPSC; MPMC needs care |
| `ConcurrentLinkedQueue` | GC language runtime managed |

Full queue policy: block producers, drop, or spin — product decision.

## Sources

- Herlihy & Shavit — concurrent queues
- Wikipedia: [Concurrent queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type))
""")

note("TTY (teletypewriter).md", """
[[Operating System]] [[file descriptors]] [[process]] [[Linux terminal]] [[Linux/login shell]]

# TTY (teletypewriter)

> A TTY is the kernel’s terminal abstraction — line discipline, session, and job control — backing terminals, SSH sessions, and pseudo-terminals (pts).

Originally hardware teletypes; now **PTY** pair: master (SSH daemon) + slave (`/dev/pts/N`) seen as stdin/stdout of [[Linux/login shell]].

```bash
tty
ps -o pid,tty,cmd
stty -a
```

**Job control** signals (SIGTSTP, Ctrl-Z) and foreground process groups depend on TTY association.

Containers without a TTY (`docker run -t`) behave differently for interactive apps.

Related: [[Linux terminal]], [[Linux/Linux terminal]].

## Sources

- Kerrisk, *The Linux Programming Interface* — terminals and sessions
- Linux `tty(4)`, `pts(4)`, `termios(3)` manual pages
- Wikipedia: [Teletypewriter](https://en.wikipedia.org/wiki/Teleprinter)
""")

note("UTS namespace.md", """
[[Operating System]] [[IPC namespace]] [[cgroup (Control Group)]] [[process]]

# UTS namespace

> The UTS namespace isolates the system hostname and NIS domain name — each container can call `sethostname` without renaming the host.

**UTS** (Unix Time-sharing System legacy name) namespace copied on `clone(CLONE_NEWUTS)` or `unshare -u`. `uname()` and `/proc/sys/kernel/hostname` reflect the namespace view.

```bash
unshare -u hostname my-container-name
hostname   # my-container-name (inside only)
```

Pair with [[IPC namespace]], PID, and mount namespaces for container identity — distinct from [[cgroup (Control Group)]] resource limits.

Requires `CONFIG_UTS_NS`; creation historically needed `CAP_SYS_ADMIN`.

## Sources

- Linux `uts_namespaces(7)` manual page
- Linux `clone(2)`, `unshare(1)` manual pages
- Wikipedia: [Linux namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)
""")

if __name__ == "__main__":
    expected = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.md"))
    written = 0
    skipped = []
    for rel, content in NOTES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1
    missing = [f for f in expected if f not in NOTES]
    extra = [f for f in NOTES if f not in expected]
    print(f"Written: {written}")
    print(f"Expected files: {len(expected)}")
    print(f"Missing from script: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  MISSING: {m}")
    if extra:
        print(f"Extra in script: {extra}")
    print(f"Skipped: {skipped}")
