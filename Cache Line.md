A **cache line** is the smallest block of memory that a CPU typically moves between **RAM and CPU cache.**
- cache line is **64 bytes** on modern CPU through the exact size depends on the CPU architecture.

```txt
┌──────────────────────────────────────────┐
│ 64 bytes                                  │
│ 1000 1001 1002 ... 1062 1063             │
└──────────────────────────────────────────┘
                    ↓
                  CPU Cache
```
- the CPU reads `A` at address `1000`, it usually doesn't fetch just `A`. It fetches the entire cache line.

Because programs commonly access **nearby memory locations.**
```go
for i := range 1000 {
	sum += array[i]
}
```

when CPU loads `arr[0]`, it gets a whole cache line containing nearby address also. Assuming each element is 4 bytes and the cache line is 64 bytes. So when the CPU subsequently needs those values are already in the cache. This is [[Spatial locality]]

## False sharing
False sharing is a CPU performance problem where multiple CPU cores modify different variables that happen to be located in the same cache line.
The variables are logically independent, the CPU cache operates on the **entire cache line**, so the cores keep invalidating each other's cached copies.
 
 **Why is it called "False" sharing?**
 Because the cores aren't actually sharing the **same variable.** They are accidentally sharing the **same cache line.**

**How do you prevent it ?**
Separate frequently modified variables into different cache lines. In low-level/high-performance code, this can be achieved through **alignment and padding.**

## Alignment and padding
**alignment and padding** are assumed to be two related ways of controlling **where data sits in memory.**
They become especially important when you're dealing with CPU cache line, structs, SIMD, and false sharing.

### Alignment
Alignment means placing data at a memory address that is a multiple of some required boundary (64-byte-alignment).

```txt
0
64
128  → aligned
192  → aligned
130  → not aligned
```
Why does it matter?
Because hardware can access data more efficiently when it is positioned according to its natural boundaries.

### Padding
Padding means inserting unused bytes between or around real data so that the data has desired layout or alignment.

```go
struct Data {
	int a; // 4 byte
	char b; // 1 byte
}
```

you might imagine: `[a][a][a][a][b]` but the **compiler** may insert unused bytes. `[a][a][a][a][b][padding][padding][padding]` So the structure occupies 8 bytes instead of 5. **The padding exists to satisfy alignment requirements.**
