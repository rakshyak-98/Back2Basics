linux OOM killer is a kernel mechanism triggered when system memory is exhausted and no more memory can be allocated.

### When it happens?
- all memory + swap used.
- kernel can't reclaim more pages.
- `malloc()` or `fork()` fails and no memory can be freed.
- kernel invokes OOM Killer to choose and kill one / more processes.

`dmesg` or `/var/log/syslog` shows killed process logs.
- `dmesg` print or control the kernel ring buffer.

```sh
dmesg | grep -i 'killed process';
```

```sh
cat /proc/kmsg; # raw stream (root only)
journalctl -k; # if systemd present
```

#### Avoid by
- adding more swap.
- tuning memory limits (e.g., cgroups for containers).
- optimizing memory usage.