Process without controlling TTY -> process not associated with any terminal (keyboard, screen).

> [!INFO]
> Normally, when you log in via terminal/SSH, a controlling terminal (tty) is assigned to your session.
> - this tty handles input/output signals, job control.

```bash
ps -o pid,tty,cmd; # TTY shows `?` when no controlling tty. 
ls -l /proc/<pid>fd/0; # if not symlinked to `/dev/tty*`, no tty attached.
```

### Process without controlling tty
- Detached from terminal, so:
	- No interactive input/output.
	- Doesn't receive terminal-generates signals (`SITINT`, `SIGHUP` on logout etc.)
	- Runs independently of any user session.
- Daemons (`sshd` `cron` `systemd` ) usually started by `init`/`systemd` without tty.
- Background jobs disowned (`nohup command` & `disown`).
- Processes launched with `setsid` -> new session, no controlling tty.
# kill process with `SIGQUIT` 
```bash
kill -s 3 <pid>; # send SIGQUIT signal
```
- the process won't show on `ps aux | grep <process sub string>;` you need to find the child process which was running instead of the process you signal `SIGQUIT`
- if the process is not still bind to the port (not released). Find and kill the child process

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

## Modern processors and RAM work together
- CPUS, operate at much higher clock speeds than RAM.
- CPU might run at speed exceeding 4 GHz, RAM typically operates at lower frequencies, such as 2133 MHz or higher depending on the generation (DDR4, DDR5).
- this discrepancy creates challenges in synchronization, as the CPU utilize techniques like caching and prefetching, which allow them to anticipate data needs and reduce the frequency of direct RAM access.
- modern processors use multiple levels of cache (L1, L2 and ... L3) to store frequently accessed data closer to the CPU.
- these reduce the ned to fetch data from RAM.
- prefetching where CPUs predict which data will be neede dnext and load it into chache before it is requested by the processor. This proactive approach helps bridge the speed gap between the CPU and RAM, allowing for smoother processing.
- Not all RAM is compatible with all CPUs. Each CPU has specific memory specifications, including supported RAM types and maximum speeds. For example, a CPU designed for DDR4 memory will not support DDR5, and if faster RAM is installed, it will typically downclock to match the maximum speed supported by the CPU

## How do multi-core processors affect RAM usage and efficiency
- Shared Memory Architecture: In multi-core systems, all cores typically share the same main memory (RAM). This shared memory model allows for efficient communication and data sharing between cores. However, it also introduces potential contention for memory access, particularly when multiple cores attempt to read from or write to the same memory location simultaneously
- Cache Hierarchies: Each core usually has its own private cache (L1), with shared caches (L2 and L3) between cores. This hierarchy helps mitigate the memory bottleneck by storing frequently accessed data closer to the processor. When a core accesses data, it first checks its cache before reaching out to the slower main RAM. This caching mechanism is crucial for maintaining high efficiency in multi-core systems, as it reduces the number of direct accesses to RAM
- Software Optimization: To fully utilize multi-core processors, software must be optimized for parallel processing. Applications that are not designed to take advantage of multiple cores may not see significant performance improvements, regardless of the hardware capabilities

# MIME
- MIME is a standard used to define the nature of the content being transferred over the internet.
- Originally developed for email, MIME type tell the browser or email client what type of content is being delivered so that it can handle it appropriately.
- this standard allows for the transmission of different types of files (like images, video, text, etc) vie email or web portocols.