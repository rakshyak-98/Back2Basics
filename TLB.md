TLB (Translation Lookaside Buffers)
Is a small, very fast cache inside the CPU/MMU that stores recent virtual address to physical-address translations.

The reason it exists is simple: The MMU would be too slow if it had to consult the page table for every memory access. The page table lives in memory, so looking it up itself requires memory accesses. That's expensive if you have to do it **every time.**

```txt
                 CPU
                  │
                  ▼
          Virtual Address
                  │
                  ▼
                TLB
           ┌──────┴──────┐
         HIT             MISS
          │                │
          │                ▼
          │          Page Table
          │                │
          └───────┬────────┘
                  ▼
          Physical Address
                  │
                  ▼
             CPU Cache
                  │
                  ▼
             Cache Line
                  │
                  ▼
                Data
```