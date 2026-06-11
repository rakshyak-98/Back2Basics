change the scheduling priority (nice value) of a running process in Linux.

## Why

CPU scheduler uses the nice value to decide which process gets more CPU time.
- Nice range: `-20` to `19`
- Lower value `-20` higher priority
- Higher value `19` lower priority
- Default `0`


> [!NOTE]
> `renice` affects CPU scheduling only

```bash
renice <nice-value> -p <pid>;
```

```bash
ps -o pid,ni,comm -p <pid>; # Check the current nice value
```