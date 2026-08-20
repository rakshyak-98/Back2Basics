# GDB : The GNU Project Debugger

[GDB](https://www.sourceware.org/gdb/) : allows you to see what is going on inside another program while it executed, or what another program was doing at the moment it crashed.

**Attach `gdb` to the running process**

```bash
sudo gdb -q -p <pid>;
```

```bash(gdb)
info proc mappings; #see the memory map, including the stack region.
x/32xg $rsp; # examine the contents of the stack pointer register and the memory it points to. 
```

```bash
(gdb) info proc
```
- **process level information about the program currently being debugged**.

```txt
process 4580
cmdline = '/home/mihir/.nvm/versions/node/v22.15.1/bin/node --require ... --import ... src/main.ts'
cwd = '/home/mihir/GitHub/DRM/backend'
exe = '/home/mihir/.nvm/versions/node/v22.15.1/bin/node'
```
- `cmdline` tells how the process is launched