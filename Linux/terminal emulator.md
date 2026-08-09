[[Linux]] [[Linux terminal]] [[CLI]]

# terminal emulator

> A terminal emulator is a GUI/TUI app that hosts a shell over a pty — Kitty, Alacritty, GNOME Terminal, xterm.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** emulator draws glyphs; kernel pty pairs bytes with the shell; terminfo tells apps how to talk.

```txt
keyboard → terminal emulator → pty → bash/zsh
                 │
            terminfo / $TERM
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **pty** | Pseudo-terminal pair | “Shell thinks it has a real TTY.” |
| **`$TERM`** | Terminfo name | “Wrong TERM = broken colors/keys.” |
| **CSI sequences** | Escape codes | “Apps move cursor / set color.” |
| **scrollback** | History buffer | “Emulator feature, not the shell.” |
| **truecolor** | 24-bit color | “Needs emulator + `$TERM` support.” |

---

## Standard config / commands

```bash
echo $TERM
infocmp | head
tty
# set size
stty size
# common emulators
# kitty, alacritty, gnome-terminal, wezterm, xterm
```

| Knob | Why it matters |
|------|----------------|
| font / ligatures | Readability; some break TUI apps |
| `$TERM` value | Must exist in terminfo on remote hosts |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Weird colors over SSH | Remote terminfo | Set `TERM=xterm-256color` or install terminfo |
| Keys insert gibberish | Terminfo mismatch | Align `$TERM`; fix bindings |
| Paste dumps escape mess | Bracketed paste | Update TUI / disable paste mode |
| Slow scroll | GPU/software render | Try another emulator; reduce effects |

---

## Gotchas

> [!WARNING]
> **Fancy `$TERM` (kitty/wezterm)** on servers without terminfo → ncurses apps implode.

> [!WARNING]
> **Multiplexers** (tmux/zsh) nest `$TERM` — set outer/inner carefully.

---

## When NOT to use

- **Pure scripts/CI** — no emulator; just pipes.
- **Serial consoles** — getty on real ttyS, not a GUI emulator.

---

## Related

[[Linux terminal]] [[terminal config]] [[CLI]] [[Bash syntax]]
