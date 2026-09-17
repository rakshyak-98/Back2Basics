Memory Management Unit.

It is a hardware component inside/alongside the CPU that translates virtual memory address used by programs into physical memory addresses in RAM.

two different process can have same virtual address, and the MMU translates it differently for each process.

```txt
Process A
0x1000
   │
   ▼
MMU → Physical RAM address 0x5000


Process B
0x1000
   │
   ▼
MMU → Physical RAM address 0x9000
```

> Virtual address `0x10001` does not mean physical RAM location `0x1000`

The MMU needs a mapping telling it where virtual memory belongs physically. The operating system maintains **page tables**

```txt
Virtual address
      │
      ▼
┌───────────────┐
│  Page Table   │
├───────────────┤
│ 0x1000 → 0x5000│
│ 0x2000 → 0x7000│
│ 0x3000 → 0x9000│
└───────────────┘
      │
      ▼
Physical RAM
```
The MMU uses these mappings when the CPU access memory.

"Modern CPU generally involves **TLBs(Translation Lookaside Buffers)** so that the CPU doesn't have to walk the page tables for every memory access. The TLB caches recent virtual -> physical translations."