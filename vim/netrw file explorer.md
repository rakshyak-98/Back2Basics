[[vim buffers]] [[Linux/CLI]]

# netrw (Vim file explorer)

> Built-in Vim directory browser (`:Explore`, `:Vex`) — navigate and open files without a plugin manager.

## Mental model

netrw is a Vim plugin (loaded by default) that renders directory listings in a buffer. `:Explore` opens netrw in the current window; `:Vex` splits vertically. Press `-` to go up a directory, `%` to create file, `d` to bookmark. It respects `netrw_liststyle` (thin/thick/long/tree).

## Standard config / commands

### Open explorer

```vim
:Explore              " current dir in current window
:Vex .                " vertical split, current dir
:Sex .                " horizontal split
:edit .               " same as Explore
```

### Navigation keys (default)

| Key | Action |
|-----|--------|
| Enter | Open file / enter dir |
| `-` | Up one directory |
| `%` | New file |
| `D` | Delete file (confirm) |
| `R` | Rename |
| `i` | Toggle list style |
| `I` | Toggle hidden files |

### Disable if using another file manager

```vim
" init.vim / .vimrc
let g:loaded_netrw = 1
let g:loaded_netrwPlugin = 1
```

### Useful options

```vim
let g:netrw_banner = 0           " hide banner
let g:netrw_liststyle = 3        " tree view
let g:netrw_winsize = 25         " Vex width %
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `:Explore` does nothing / error | `echo g:loaded_netrw` | Re-enable netrw; check plugin manager didn't block it |
| Slow on remote dirs | SSHFS / NFS latency | Use `ranger`/`lf` in terminal split instead |
| Wrong cwd | `:pwd` | `:cd /path` then `:Explore` |
| Tree view broken | `netrw_liststyle` | Set to 3; update Vim (old netrw bugs) |
| Accidental delete | `netrw_fastbrowse` | Set `let g:netrw_fastbrowse = 0` for confirm |

## Gotchas

> [!WARNING]
> **`D` deletes immediately** in some configs — muscle memory from `:bd` doesn't apply.
>
> **netrw + autochdir** — plugins that `cd` on buffer switch confuse relative paths.

## When NOT to use

- Don't fight netrw if you live in fuzzy finders — disable it and use fzf/telescope in Neovim.
- Don't use netrw as a project-wide search tool — `:grep`/LSP is better.

## Related

[[vim buffers]] [[Linux/commands/fzf]] [[Descriptive/vscode]]
