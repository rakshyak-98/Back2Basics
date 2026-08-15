[[Linux terminal]] [[login shell]] [[CLI]] [[terminal config]] [[editor config]] [[SSH]] [[puTTY]]

# terminal emulator

> Renders monospace text and turns keystrokes into bytes for a shell on a pseudo-terminal (PTY).

## Interview Relevance

Shows you know `$TERM`/terminfo, PTY allocation over SSH, and that PuTTY/Alacritty are emulators — not shells.

## Sources

- `man 1 xterm` — overview
- [VTE library (GNOME terminal core)](https://wiki.gnome.org/Apps/Terminal/VTE) — deep-dive

## Core Definition

Popular emulators (GNOME Terminal, Konsole, Alacritty, Kitty, xterm) implement DEC VT-style escape sequences so TUI apps ([[top]], vim, htop) can move the cursor and use colors.

## Key Concepts

- **Emulator ≠ shell:** the emulator draws; bash/zsh interpret.
- **`$TERM` + terminfo:** mismatch breaks layouts and colors.
- **PTY:** SSH allocates one by default (`ssh -t`).
- **GPU emulators:** Alacritty/Kitty trade features for speed.

## Technical Details

```bash
gnome-terminal
alacritty -e bash
infocmp xterm-256color | head
export TERM=xterm-256color
```

Typical settings: font (Nerd Font for icons), scrollback size, copy-on-select, shell command (`-e`), transparency (compositor needed on X11).

[[SSH]] allocates a PTY by default. [[puTTY]] on Windows is a terminal emulator plus SSH client.

## Real-World Applications

Fix broken ncurses UIs over SSH by aligning remote `$TERM` with installed terminfo, or fall back to `xterm-256color`.

## Pros/Cons or Trade-offs

- **Pro:** Portable TUI world via escape sequences.
- **Con:** Terminfo mismatches and font glyph gaps cause “broken” apps that are fine in another emulator.

## Comparison

- vs [[Linux terminal]]: broader terminal/TTY concept; this note is the GUI/app that hosts it.
- vs real hardware VT: emulators approximate; serial consoles still matter for recovery.

## Mistakes to Avoid

- Setting exotic `$TERM` values the remote host lacks.
- Confusing the emulator with the login shell configuration.
- Expecting X11 transparency without a compositor.
