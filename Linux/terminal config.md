[[terminal emulator]] [[Linux terminal]] [[editor config]] [[gnome Colorschem]] [[Bash/Bash history]]

# terminal config

> Fonts, colors, shell startup, and multiplexer settings — the knobs that make daily CLI work comfortable.

## Interview Relevance

Ops comfort signal: login vs interactive startup files, `$TERM`, and a portable tmux/shell profile for jump boxes.

## Sources

- `man 1 bash` (INVOCATION) — deep-dive
- [tmux man page](https://man.openbsd.org/tmux.1) — overview

## Key Concepts

- **Startup chain:** profile for login; bashrc for interactive non-login.
- **Prompt / history:** `PS1`, `HISTSIZE`, `histappend`.
- **Multiplexer:** tmux/screen survive SSH drops.
- **Emulator configs:** Alacritty/Kitty/GNOME Terminal each have their own files.

## Technical Details

| File | When |
|------|------|
| `/etc/profile` | Login shells |
| `~/.bash_profile` / `~/.profile` | User login |
| `~/.bashrc` | Interactive non-login Bash |
| `~/.bash_logout` | Logout |

```bash
grep -n bashrc ~/.profile
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\w\$ '
export HISTSIZE=50000
export HISTCONTROL=ignoreboth
shopt -s histappend
```

```bash
# ~/.tmux.conf
set -g mouse on
set -g default-terminal "screen-256color"
setw -g mode-keys vi
```

| Emulator | Config |
|----------|--------|
| Alacritty | `~/.config/alacritty/alacritty.toml` |
| GNOME Terminal | `dconf` / profile GUI |
| Kitty | `~/.config/kitty/kitty.conf` |

## Real-World Applications

Golden laptop image: shared `.bashrc` + `.tmux.conf` so every engineer gets the same history and mouse-enabled tmux on day one.

## Pros/Cons or Trade-offs

- **Pro:** Huge daily productivity leverage for little cost.
- **Con:** Over-custom configs break on minimal rescue environments — keep a lean fallback.

## Comparison

- vs [[terminal emulator]]: the app that draws glyphs; this note is settings for shell + emulator.
- vs [[editor config]]: buffers/keybindings vs terminal chrome and shell environment.

## Mistakes to Avoid

- Putting PATH only in interactive bashrc and missing cron/SSH non-interactive jobs.
- Setting `default-terminal` to values the remote host terminfo lacks.
- Typos in Alacritty path (`alicritty.toml`) that silently do nothing.
