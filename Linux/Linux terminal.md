[[Linux]] [[terminal emulator]] [[CLI]] [[login shell]]

# Linux terminal

> A Linux terminal is the text I/O path to a shell — local emulator, TTY/getty, or SSH session over a pty.

## Mental model

**Say it in one breath:** bytes on a pty; line discipline handles canonical mode/signals; apps query size via `TIOCGWINSZ`.

```txt
SSH/emulator → pty slave → shell → child cmds
                 │
            stty / termios
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **TTY** | Terminal device | “`tty` prints the device path.” |
| --- | --- | --- |
| **pty** | Pseudo-terminal | “SSH and GUI terminals use ptys.” |
| **job control** | fg/bg/Ctrl-Z | “Shell manages process groups.” |
| **signals** | Ctrl-C → SIGINT | “Line discipline generates signals.” |
| **raw vs canonical** | Char vs line mode | “TUIs switch to raw.” |

## Standard config / commands

```bash
tty
stty -a
stty size
script -q /tmp/session.log   # record
# reset broken terminal
reset
tput remcup; tput clear
```

| Knob | Why it matters |

| `stty sane` | Recover after binary dump |
| --- | --- |
| `COLUMNS`/`LINES` | Some apps skip ioctl |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Garbled screen | Binary / bad terminfo | `reset`; fix `$TERM` |
| No job control | Not a tty | Allocate pty (`ssh -t`) |
| Backspace prints `^H` | Erase char | `stty erase ^?` |
| Resize broken | SIGWINCH ignored | Fix app; update ncurses |

## Gotchas

> [!WARNING]
> **Redirected stdin is not a TTY** — prompts and sudo may fail; use `ssh -t` or `script`.

> [!WARNING]
> **`kill` vs terminal signals** — Ctrl-C hits the foreground process group, not arbitrary PIDs.

## When NOT to use

- **Machine APIs** — prefer SSH+command, agents, or HTTP over interactive terminals.
- **Binary protocols** — don’t shove them through a cooked TTY.

## Related

[[terminal emulator]] [[terminal configuration]] [[CLI]] [[login shell]] [[SSH]]
