[[CLI]] [[login shell]] [[terminal emulator]] [[terminal config]] [[editor config]] [[SSH]]

# Linux terminal

> The Linux terminal is the character-cell interface to the shell — emulator + PTY + shell, whether on a local TTY or remote over SSH.

```txt
        Linux terminal ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Everyday ops fluency: `$TERM`, PTY vs TTY, why colors break in tmux, and how …

## Sources
- `man 4 tty`, `man 7 pty` — deep-dive
- [ANSI escape codes / ECMA-48](https://en.wikipedia.org/wiki/ANSI_escape_code) — overview

## Key Concepts
- **Emulator vs shell:** Alacritty/GNOME Terminal display cells; Bash/Zsh interpret commands.
- **PTY:** Kernel pair that makes programs think they have a real teletype.
- **TERM:** Capability database key (`xterm-256color`, `alacritty`, `screen-256color`).
- **Multiplexer:** tmux/screen add detachable sessions on top of a PTY.
- **Remote:** [[SSH]] allocates a PTY for interactive sessions.


- **Core:** Stack: **terminal emulator** (or serial console) ↔ **pseudo-terminal (PTY)** …

## Technical Details
| Piece | Example |
|-------|---------|
| Emulator | GNOME Terminal, Alacritty, [[puTTY]] |
| Shell | Bash, Zsh |
| Multiplexer | tmux, screen |
| Remote | [[SSH]] |

```bash
echo $TERM          # xterm-256color, alacritty, screen.xterm-256color
tput colors         # 256 on modern setups
stty size           # rows cols
```

| Symptom | Fix |
|---------|-----|
| Broken colors in `ls` | `export TERM=xterm-256color`; install `ncurses-term` |
| Keys don't work in tmux | `TERM=screen-256color` inside tmux; fix `~/.tmux.conf` |
| Narrow wrap / garbled output | `reset` or `stty sane` |
| SSH disconnect kills job | `tmux` or `systemd-run --user` |

## Mistakes to Avoid
- **Mistake:** Setting `TERM=xterm-256color` inside tmux when `screen-256color`…
- **Mistake:** Running long jobs on a raw SSH PTY without tmux/screen
- **Mistake:** Ignoring `stty sane` / `reset` when the terminal is merely desyn…

## Pros/Cons or Trade-offs
- **Pro:** Universal remote administration surface; works when GUIs cannot.
- **Con:** Capability mismatches (`TERM`) cause subtle UI bugs; easy to lose work without a multiplexer.

## Comparison
- vs [[CLI]]: terminal is the display/input path


### Use cases
- An engineer SSHs to a bastion, attaches tmux with a correct `TERM`, and leave…
