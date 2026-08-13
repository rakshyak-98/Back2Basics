[[CLI]] [[login shell]] [[terminal emulator]] [[terminal config]]

# Linux terminal

> The Linux terminal is the character-cell interface to the shell — emulator + PTY + shell, whether local on a TTY or remote over SSH.

Stack: **terminal emulator** (or serial console) ↔ **pseudo-terminal (PTY)** ↔ **shell** ([[login shell]]) ↔ kernel. Environment variables (`TERM`, `COLORTERM`) tell programs how to draw colors and cursor motion.

## Components

| Piece | Example |
|-------|---------|
| Emulator | GNOME Terminal, Alacritty, [[puTTY]] |
| Shell | Bash, Zsh |
| Multiplexer | tmux, screen |
| Remote | [[SSH]] |

## Verify terminal type

```bash
echo $TERM          # xterm-256color, alacritty, screen.xterm-256color
tput colors         # 256 on modern setups
stty size           # rows cols
```

## Common issues

| Symptom | Fix |
|---------|-----|
| Broken colors in `ls` | `export TERM=xterm-256color`; install `ncurses-term` |
| Keys don't work in tmux | `TERM=screen-256color` inside tmux; fix `~/.tmux.conf` |
| Narrow wrap / garbled output | Reset: `reset` or `stty sane` |
| SSH disconnect kills job | Use `tmux` or `systemd-run --user` |

## Related

[[terminal emulator]] · [[terminal config]] · [[CLI]] · [[editor config]]

## Sources

- `man 4 tty`, `man 7 pty`
- [ECMA-48 / ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code)
