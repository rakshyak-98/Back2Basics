```bash
sudo apt install strace;
```

```bash
strace -c <command>; # trace system call and signals
strace <path of executable file>;
```

```bash
cat /proc/<pid>/maps; # memory map of the process
```

```text
7fff17093000-7fff170b4000 rw-p 00000000 00:00 0 [stack]
```
- the line containing the `[stack]` in the path column shows the memory region used for the stack.
- the start and end addresses of the stack are shown in the *first column*, separated by a hyphen.
- the permissions are shown in the second column. For the stack, it's typically `rw-p` (read, write, private).

```bash
pmap <pid>
```


### gdb
1. Attach `gdb` to the running process
```bash
gdb -p <pid>;
```

```bash(gdb)
info proc mappings; #see the memory map, including the stack region.
x/32xg $rsp; # examine the contents of the stack pointer register and the memory it points to. 
```