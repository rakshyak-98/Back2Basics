```bash
lscpu -C
```

```txt
➜  dsa-problem git:(main) lscpu -C
NAME ONE-SIZE ALL-SIZE WAYS TYPE        LEVEL SETS PHY-LINE COHERENCY-SIZE
L1d       32K     128K    8 Data            1   64        1             64
L1i       32K     128K    8 Instruction     1   64        1             64
L2       256K       1M    4 Unified         2 1024        1             64
L3         8M       8M   16 Unified         3 8192        1             64
```

## CPU Cache L1, L2, L3... Ln
CPU cache L1, l2, L3 are levels of memory physically close to the CPU cores. They exist because **CPU execution is dramatically faster than accessing main RAM.**

```txt
CPU Core
  │
  ├── Registers          ← smallest, fastest
  │
  ├── L1 Cache          ← very small, extremely fast
  │
  ├── L2 Cache          ← larger, slower
  │
  ├── L3 Cache          ← much larger, slower
  │
  └── RAM               ← huge, much slower
```
- each level as another opportunity to find data **before going all the way to RAM.**

"Making a cache extremely fast requires keeping it physically and logically close to the execution units."

> [!INFO]
> A major architectural characteristic of L3 is that it is often **shared between multiple cores.**

**Why does this hierarchy exist?**
Because you can't simply build one enormous, ultra-fast cache. As memory become larger and farther from the CPU, making every access extremely fast becomes increasingly expensive. So CPU use **multiple levels**
- The CPU isn't accessing completely random memory every time. It accesses nearby memory repeatedly. That allows the CPU to bring a **cache line** into cache rather than fetching every individual byte from RAM.

> [!NOTE]
> The **CPU hardware and memory subsystem** handle CPU-cache placement automatically.

[[Swap memory]] live below RAM. L1/L2/L3 are inside the CPU memory hierarchy; swap is an OS-level mechanism.

> If the required memory page **isn't currently in RAM**, then the OS may have to deal with swap