[[terminal emulator]] [[Linux terminal]] [[editor config]]

# terminal config

> Terminal configuration covers fonts, colors, shell startup, and multiplexer settings — the knobs that make daily CLI work comfortable.

## Shell startup chain

| File | When |
|------|------|
| `/etc/profile` | Login shells |
| `~/.bash_profile` / `~/.profile` | User login |
| `~/.bashrc` | Interactive non-login Bash |
| `~/.bash_logout` | Logout |

```bash
# Typical: login profile sources bashrc
grep -n bashrc ~/.profile
```

## Prompt and history

```bash
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\w\$ '
export HISTSIZE=50000
export HISTCONTROL=ignoreboth
shopt -s histappend
```

See [[Bash history]] for persistence across sessions.

## tmux

```bash
# ~/.tmux.conf
set -g mouse on
set -g default-terminal "screen-256color"
setw -g mode-keys vi
```

## Emulator config paths

| Emulator | Config |
|----------|--------|
| Alacritty | `~/.config/alacritty/alicritty.toml` |
| GNOME Terminal | `dconf` / profile GUI |
| Kitty | `~/.config/kitty/kitty.conf` |

## Related

[[terminal emulator]] · [[editor config]] · [[gnome Colorschem]] · [[Bash history]]

## Sources

- `man 1 bash` — INVOCATION section
- [tmux man page](https://man.openbsd.org/tmux.1)
