[[Linux/CLI]] [[Linux/Scripting]]

# tmux copy-mode

> Keyboard selection + copy from scrollback into tmux paste buffers — essential before yanking to system clipboard.

## Mental model

tmux maintains a scrollback per pane. **Copy-mode** enters a vi/emacs-like overlay to move, select, and yank text into a **paste buffer** (internal register). From there, paste into pane (`paste-buffer`) or sync to system clipboard (config-dependent). Copy-mode is not the same as shell `Ctrl+Shift+C`.

```
Pane scrollback → copy-mode → selection → paste buffer → paste / save-buffer
```

## Standard config / commands

### Enter copy-mode (default prefix `Ctrl+b`)

```txt
Prefix + [          " enter copy-mode
q                   " quit copy-mode
```

### Vi keys (if `mode-keys vi` in ~/.tmux.conf)

```txt
Space               " start selection
Enter               " copy selection to paste buffer
Esc                 " cancel
/                   " search forward
n / N               " next/prev match
```

### Paste buffer management

```txt
Prefix + ]          " paste most recent buffer into pane
tmux show-buffer
tmux save-buffer ~/copied.txt
tmux load-buffer ~/file.txt
tmux list-buffers
tmux delete-buffer -a
```

### Clipboard integration (~/.tmux.conf)

```tmux
set -g mode-keys vi
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can't enter copy-mode | Wrong prefix | `Prefix + [` ; verify `prefix` in conf |
| Yank does nothing | `mode-keys` | Set vi/emacs keys; use Enter after selection |
| Paste empty | `list-buffers` | Re-yank; copy-mode exited early |
| No system clipboard | `xclip`/`wl-copy` missing | Install xclip; add `copy-pipe` bind |
| Mouse scroll weird | `mouse on` | `set -g mouse on` + proper terminal |
| Wrong buffer pasted | `show-buffer` | Use `-b N` with save-buffer |

## Gotchas

> [!WARNING]
> **SSH without X11** — system clipboard bridge won't work; use `save-buffer` to file.
>
> **Large selection** — tmux buffer limits; pipe to file for big logs.
>
> **Copy-mode vs terminal copy** — selecting with mouse may bypass tmux buffer depending on `terminal-overrides`.

## When NOT to use

- Don't copy secrets from prod logs into shared clipboard on untrusted machines.
- Don't rely on copy-mode in fully mouse-driven workflows without learning prefix keys — you'll fight the tool.

## Related

[[Linux/CLI]] [[Linux/commands/fzf]] [[ssh/ssh allow local system with key]]
