[[vim buffers]] [[vim commands]] [[Linux/commands/fzf]] [[Linux/CLI]]

# netrw file explorer

> Built-in Vim directory browser (`:Explore`, `:Vex`) — open and manage files without a plugin manager.

```txt
        netrw file explore ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you can navigate a remote host with stock Vim

## Sources
- [Vim help — pi_netrw](https://vimhelp.org/pi_netrw.txt.html) — deep-dive
- [Wikipedia — netrw](https://en.wikipedia.org/wiki/Netrw) — overview

## Key Concepts
- **Explore family:** `:Explore`, `:Vexplore` / `:Vex`, `:Sexplore` / `:Sex`, `:Lexplore` → same br…
- **Remote URLs:** `vim scp://user@host/path/` → edit over SSH without leaving Vim.
- **List styles:** thin / long / wide / tree (`i` cycles
- **Buffers still rule:** netrw is a buffer; [[vim buffers]] commands (`:bd`, `:ls`) apply


- **Core:** netrw is Vim’s shipped plugin for local and remote directory listing. It load…

## Technical Details
```vim
:Explore              " current file's directory (or cwd)
:Vex .                " vertical split explorer
:Sex .                " horizontal split
:Lexplore             " toggle left drawer-style explorer
:edit .               " same idea as Explore
```

| Key | Action |
|-----|--------|
| Enter | Open file / enter directory |
| `-` | Parent directory |
| `%` | New file |
| `d` | New directory |
| `D` | Delete (confirm) |
| `R` | Rename |
| `i` | Cycle list style |
| `I` / `gh` | Toggle banner / hide dotfiles (version-dependent) |

```vim
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_winsize = 25

" disable if using another file manager
let g:loaded_netrw = 1
let g:loaded_netrwPlugin = 1
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `:Explore` does nothing | `echo g:loaded_netrw` | Re-enable; plugin manager may have blocked it |
| Slow on remote dirs | SSHFS / NFS latency | Terminal file manager in a split instead |
| Wrong working directory | `:pwd` | `:cd /path` then `:Explore` |
| Accidental delete | Confirm prompts | Prefer `g:netrw_fastbrowse = 0`; double-check before `D` |

## Mistakes to Avoid
- **Mistake:** Muscle-memory `D` thinking it is `:bd`
- **Mistake:** Fighting netrw while using autochdir plugins
- **Mistake:** Using netrw as project-wide search

## Pros/Cons or Trade-offs
- **Pro:** Zero install; local + remote protocols in one tool.
- **Con:** UX is dated; fuzzy finders ([[Linux/commands/fzf]], Telescope) win for large trees.

## Comparison
- vs NERDTree / oil.nvim: plugins polish UX; netrw is always there.
- vs `fzf` / Telescope: search-by-name beats tree browsing for large codebases.


### Use cases
- Onboarding a bastion host with only Vim installed
