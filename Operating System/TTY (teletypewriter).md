[[Operating System]] [[file descriptors]] [[process]] [[Linux terminal]] [[Linux/login shell]]

# TTY (teletypewriter)

> A TTY is the kernel’s terminal abstraction — line discipline, session, and job control — backing terminals, SSH sessions, and pseudo-terminals (pts).

Originally hardware teletypes; now **PTY** pair: master (SSH daemon) + slave (`/dev/pts/N`) seen as stdin/stdout of [[Linux/login shell]].

```bash
tty
ps -o pid,tty,cmd
stty -a
```

**Job control** signals (SIGTSTP, Ctrl-Z) and foreground process groups depend on TTY association.

Containers without a TTY (`docker run -t`) behave differently for interactive apps.

Related: [[Linux terminal]], [[Linux/Linux terminal]].

## Sources

- Kerrisk, *The Linux Programming Interface* — terminals and sessions
- Linux `tty(4)`, `pts(4)`, `termios(3)` manual pages
- Wikipedia: [Teletypewriter](https://en.wikipedia.org/wiki/Teleprinter)
