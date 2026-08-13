[[Linux terminal]] [[login shell]] [[CLI]]

# terminal emulator

> A terminal emulator renders monospace text and translates keystrokes into bytes for a shell running on a pseudo-terminal.

Popular emulators: **GNOME Terminal**, **Konsole**, **Alacritty** (GPU), **Kitty**, **xterm** (reference). They implement **DEC VT**-style escape sequences so TUI apps ([[top]], `vim`, `htop`) can move the cursor and use colors.

## Choose / configure

```bash
# Default on GNOME
gnome-terminal

# GPU-accelerated
alacritty -e bash
```

Typical settings: font (Nerd Font for icons), scrollback size, copy-on-select, shell command (`-e`), transparency (compositor needed on X11).

## `TERM` environment

Programs query terminfo via `$TERM`. Mismatch causes broken layouts:

```bash
infocmp xterm-256color | head
export TERM=xterm-256color   # safe default when unsure
```

## Remote terminals

[[SSH]] allocates a PTY by default (`ssh -t`). [[puTTY]] on Windows is a terminal emulator plus SSH client.

## Related

[[terminal config]] · [[Linux terminal]] · [[editor config]]

## Sources

- `man 1 xterm`
- [VTE library (GNOME terminal core)](https://wiki.gnome.org/Apps/Terminal/VTE)
