[[Linux terminal]] [[login shell]] [[CLI]] [[terminal config]] [[editor config]] [[SSH]] [[puTTY]]

# terminal emulator

> Renders monospace text and turns keystrokes into bytes for a shell on a pseudo-terminal (PTY).

```txt
        terminal emulator ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you know `$TERM`/terminfo, PTY allocation over SSH, and that PuTTY/Alac…

## Sources
- `man 1 xterm` — overview
- [VTE library (GNOME terminal core)](https://wiki.gnome.org/Apps/Terminal/VTE) — deep-dive

## Key Concepts
- **Emulator ≠ shell:** the emulator draws; bash/zsh interpret.
- **`$TERM` + terminfo:** mismatch breaks layouts and colors.
- **PTY:** SSH allocates one by default (`ssh -t`).
- **GPU emulators:** Alacritty/Kitty trade features for speed.


- **Core:** Popular emulators (GNOME Terminal, Konsole, Alacritty, Kitty, xterm) implemen…

## Technical Details
```bash
gnome-terminal
alacritty -e bash
infocmp xterm-256color | head
export TERM=xterm-256color
```

- Typical settings: font (Nerd Font for icons), scrollback size, copy-on-select…

- [[SSH]] allocates a PTY by default.
- [[puTTY]] on Windows is a terminal emulator plus SSH client.

## Mistakes to Avoid
- **Mistake:** Setting exotic `$TERM` values the remote host lacks
- **Mistake:** Confusing the emulator with the login shell configuration
- **Mistake:** Expecting X11 transparency without a compositor

## Pros/Cons or Trade-offs
- **Pro:** Portable TUI world via escape sequences.
- **Con:** Terminfo mismatches and font glyph gaps cause “broken” apps that are fine in another emulator.

## Comparison
- vs [[Linux terminal]]: broader terminal/TTY concept; this note is the GUI/app that hosts it.
- vs real hardware VT: emulators approximate; serial consoles still matter for recovery.


### Use cases
- Fix broken ncurses UIs over SSH by aligning remote `$TERM` with installed ter…
