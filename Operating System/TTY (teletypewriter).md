[[Operating System]] [[file descriptors]] [[OS program]]

# TTY (teletypewriter)

> A TTY is a terminal device — keyboard in, text out; modern shells use a pty (pseudo-TTY) pair behind the emulator.

## Mental model

**Say it in one breath:** Line discipline turns bytes into canonical input; `/dev/ttyN` are virtual consoles; `/dev/pts/N` are pts slaves for terminal apps/SSH.

```txt
xterm / sshd
   │
   ├─ master (/dev/ptmx)  ← emulator / sshd writes/reads
   └─ slave  (/dev/pts/N) ← shell’s stdin/stdout/stderr
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **TTY** | Terminal device abstraction | “Job control and signals hang off a controlling tty.” |
| --- | --- | --- |
| **PTY** | Pseudo-TTY pair | “Software tty for emulators and SSH.” |
| **PTS** | Slave side under `/dev/pts` | “`tty` prints `/dev/pts/3` in GNOME Terminal.” |
| **VT** | Virtual console | “Ctrl+Alt+F3 drops to text console.” |
| **Line discipline** | Kernel input processing | “Canonical mode buffers until Enter.” |
| **Controlling terminal** | Session’s tty | “Ctrl+C →SIGINT to foreground group.” |

### How the story goes

1. **Open** — login or emulator allocates a tty/pty.
2. **Session** — shell becomes session leader; tty is controlling.
3. **I/O** — reads/writes go through line discipline (+ termios flags).
4. **Signals** — kernel maps break/resize to SIGINT/SIGWINCH, etc.

## Standard config / commands

```bash
tty                          # current device
who                          # who’s on which tty
ls /dev/pts /dev/tty*        # devices
stty -a                      # termios settings
script /tmp/typescript       # record a session (uses pty)
# Virtual consoles: Ctrl+Alt+F1…F6; GUI often F1 or F7 depending on distro
```

| Knob | Why it matters |

| `stty raw` / `cooked` | Pass-through vs line editing |
| --- | --- |
| `TOSTOP` | Background writes → SIGTTOU |
| `pts` limit | Many SSH/tmux sessions |
| `mesg` / `wall` | Write to others’ ttys |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `not a tty` in scripts | stdin is pipe | Don’t require tty; or `ssh -t` |
| No Ctrl+C | Wrong process group / raw mode | Restore cooked; fix job control |
| Garbled UI after binary | Terminal modes trashed | `reset` / `stty sane` |
| Can’t open `/dev/pts` | Devpts not mounted / quota | Remount `devpts`; raise limits |
| SSH hangs without prompt | Allocated tty vs command mode | `-t`/`-T` deliberately |
| Console login broken | getty down | `systemctl status getty@tty1` |

## Gotchas

> [!WARNING]
> **Docker `-t` without `-i`** — weird stdin; CI often wants neither.

> [!WARNING]
> **Logging passwords** — tools that force a tty can still leak via `script`/asciinema.

> [!WARNING]
> **`/dev/tty` vs stdin** — open `/dev/tty` talks to controlling terminal even if stdin is redirected.

> [!WARNING]
> **Mobile “TTY mode”** — accessibility feature; unrelated to Unix pty.

## When NOT to use

- **Machine-to-machine APIs** — plain pipes/sockets; no line discipline.
- **Structured logs to journal/file** — don’t pretend daemons need a tty.
- **Binary protocols** — disable canonical processing or avoid tty entirely.

## Related

[[file descriptors]] [[discriptors]] [[OS program]] [[system call]] [[Linux Process Theory]]
