[[vim]] [[vim commands]] [[vim keybindings]]

# vim config

> Vim reads `~/.vimrc` at startup — clipboard, indentation, and search behavior depend on compile-time features and the packages you install.

## Mental model

**Say it in one breath:** Check `vim --version` for `+clipboard` before relying on `set clipboard`; without it, install `vim-gtk3` (or Neovim) and point `unnamedplus` at your system clipboard helper.

```bash
vim --version | grep clipboard
# +clipboard  → set clipboard=unnamedplus works
# -clipboard  → install vim-gtk3 or use Neovim
```

### Standard settings

```vim
set autoindent
set smartindent
set clipboard=unnamedplus
set expandtab
set shiftwidth=4
set tabstop=4
set incsearch
set ignorecase
set smartcase
syntax on
filetype indent on
```

| Setting | Purpose |
| --- | --- |
| `clipboard=unnamedplus` | Yank/paste via system clipboard (needs `+clipboard`) |
| `expandtab` + `shiftwidth=4` | Tabs become four spaces; `>>` / `<<` indent by four |
| `smartcase` | Case-sensitive search when the pattern contains uppercase |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `+clipboard` missing | `vim --version \| grep clipboard` | `sudo apt install vim-gtk3` or switch to Neovim |
| Paste does nothing | `xclip` / `wl-clipboard` installed | Install clipboard bridge; restart terminal |
| Indentation inconsistent | `:set et? sw? ts?` | Set `expandtab`, `shiftwidth`, `tabstop` together |
| Settings ignored | Wrong config file loaded | `:echo $MYVIMRC`; confirm `~/.vimrc` path |

## Gotchas

> [!WARNING]
> **Even with `xclip` installed**, Vim without `+clipboard` cannot bridge to the system clipboard — the feature is compile-time, not a plugin.

> [!WARNING]
> **`tabstop` vs `shiftwidth`** — comments in old notes sometimes disagree; `expandtab` makes `<Tab>` insert `shiftwidth` spaces.

## When NOT to use

- **Heavy IDE features in Vim** — use LSP plugins or an IDE when refactoring across dozens of files is the daily job.
- **Duplicating Neovim Lua config in Vimscript** — pick one editor for your main setup.

## Related

[[vim commands]] [[vim keybindings]] [[vim buffers]] [[nvim setup]]
