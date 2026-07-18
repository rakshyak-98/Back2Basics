- in-memory circular log used for kernel messages.
A circular buffer in the Linux kernel used to store log messages, primarily for debugging and boot-time logs.

- Kernel `printk()` messages
- [[OOM (Linux Out Of Memory)]] Killer logs
- Drive logs
- Early boot messages (before `syslog` daemon starts)

- fixed-size buffer
- old messages overwritten by new ones when full
- prevents memory overflow