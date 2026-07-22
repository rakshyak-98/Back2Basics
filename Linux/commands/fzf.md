[[Linux terminal]] [[bash script]] [[Find command]]

# fzf

> One-line: fuzzy finder for the terminal — filter any list interactively (files, history, processes, git branches) with sub-100ms feel. **Reach for it when Tab completion isn't enough.**

## Mental model

`fzf` reads stdin (or a shell hook), scores lines against your typed fuzzy pattern, shows an interactive TUI. It's a **filter**, not a search engine — you pipe candidates in, pick one out via `$()` or key bindings.

```
find / ls / history ──► fzf ──► selected line ──► cd / vim / kill
         ▲
    Ctrl+R / Ctrl+T (shell integration)
```

| Integration | Trigger | Action |
|-------------|---------|--------|
| Shell history | `Ctrl+R` | Fuzzy reverse search |
| File path | `Ctrl+T` | Insert file path |
| `cd` | `Alt+C` | Jump to directory |
| Generic | `cmd \| fzf` | Filter any list |

Install: `apt install fzf` (Debian/Ubuntu) — enable shell hooks via `/usr/share/doc/fzf/examples/key-bindings.bash`.

## Standard config / commands

```bash
# Basic filter
ls | fzf
find . -type f | fzf

# Open selected file in editor
vim "$(find . -type f | fzf)"

# Kill process by name
ps aux | fzf | awk '{print $2}' | xargs kill

# Git branch checkout
git branch | fzf | xargs git checkout

# Preview file content while browsing
fzf --preview 'cat {}' --preview-window=right:50%

# Multi-select (Tab to mark, Enter to confirm)
fzf -m

# Respect .gitignore (with fd — faster than find)
fd . | fzf

# Environment tuning
export FZF_DEFAULT_COMMAND='fd --type f'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'
```

**Production-safe patterns:**

```bash
# Safe cd — only directories
cd "$(find . -type d | fzf)"

# SSH host from known_hosts
grep '^Host ' ~/.ssh/config | awk '{print $2}' | fzf | xargs -I{} ssh {}

# Journal unit picker
systemctl list-units --type=service --no-pager | awk '{print $1}' | fzf | xargs journalctl -u -f
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `fzf: command not found` | Not installed | `apt install fzf` / `brew install fzf` |
| Ctrl+R still default bash search | Hooks not sourced | Add `source /usr/share/fzf/key-bindings.bash` to `.bashrc` |
| Empty list | Upstream pipe empty | Test pipe alone: `find . \| head` |
| Garbled TUI | Wrong `TERM` | `export TERM=xterm-256color`; use UTF-8 locale |
| Slow on huge trees | `find /` from root | Scope to project; use `fd`; set `FZF_DEFAULT_COMMAND` |
| `xargs` ran wrong command | Blank or multi-column input | Quote: `fzf \| xargs -r -I{} cmd {}` |

## Gotchas

> [!WARNING]
> **`xargs` without `-r` / confirmation on destructive ops** — `fzf | xargs rm` is foot-gun. Preview first; use `-r` (GNU).

> [!WARNING]
> **Paths with spaces** — always `"$(fzf)"` quoted; use `-0` / `fd -0` / `fzf --read0` for null-delimited.

> [!WARNING]
> **SSH over slow link** — fzf needs decent terminal latency; plain grep may be faster over high-latency sessions.

> [!WARNING]
> **Non-interactive scripts** — fzf needs a TTY; don't pipe it in CI without `/dev/tty` hack.

## When NOT to use

- **Scripted automation (no human)** → fixed paths, `find -name`, `rg`.
- **Server without TTY** → avoid; use completion or explicit args.
- **Security-sensitive host enumeration** — interactive browsing of `/etc` leaves audit trail of intent; use targeted commands.

## Related

[[Linux terminal]] [[Find command]] [[bash script]] [[grep]] [[CLI]]
