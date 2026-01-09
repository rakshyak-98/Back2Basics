
## How process memory spaces work in Linux (modern x86-64)

> [!INFO]
> Every process in Linux gets its own virtual address space. An illusion of having almost the entire memory for itself.
> Process sees only virtual addresses.


```bash
cat /proc/<pid>/maps          # memory regions + permissions
pmap -XX <pid>                # more human readable
gdb -p <pid> → (gdb) info proc mappings
```