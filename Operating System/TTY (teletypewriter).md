[[Operating System]] [[process]] [[Linux terminal]] [[login shell]] [[file descriptors]]

# TTY (teletypewriter)

> A TTY is the kernel’s terminal abstraction — line discipline, session, and job control — backing consoles, SSH sessions, and pseudo-terminals (pts).

```txt
        TTY (teletypewrite ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Ops/systems questions: PTY master/slave, why `docker run -t` matters, and how…

## Sources
- Kerrisk, *The Linux Programming Interface* — terminals and sessions — deep-dive
- Linux `tty(4)`, `pts(4)`, `termios(3)` manual pages — deep-dive
- [Wikipedia — Teletypewriter](https://en.wikipedia.org/wiki/Teleprinter) — overview

## Key Concepts
- **Historical teletype → modern PTY:** master (SSH daemon) + slave (`/dev/pts/N`).
- **Line discipline:** canonical vs raw modes (`termios`).
- **Session / job control:** foreground process group, SIGTSTP, Ctrl-C.
- **fds 0/1/2:** usually connected to the TTY for interactive [[login shell]].

## Technical Details
```bash
tty
ps -o pid,tty,cmd
stty -a
```

- Containers without a TTY (`docker run -t`) behave differently for interactive…

- Related: [[Linux terminal]], [[login shell]].

## Mistakes to Avoid
- **Mistake:** Detecting interactivity only via `isatty(1)` and then breaking l…
- **Mistake:** Forgetting `-t`/`-i` in containers and blaming the app for missi…
- **Mistake:** Sending binary protocols through a cooked TTY without raw mode

## Pros/Cons or Trade-offs
- **Pro:** Job control and line editing “just work” for humans.
- **Con:** Programs that assume a TTY break in pipelines and non-interactive CI.
- **Trade-off:** allocating PTYs in orchestration vs simpler pipe-only I/O.

## Comparison
- vs plain pipes: pipes have no line discipline or job control.
- vs [[file descriptors]]: TTY is a special character device behind those fds.


### Use cases
- SSH sessions, `screen`/`tmux`, CI that allocates a pseudo-TTY for progress ba…
