[[vim commands]] [[vim buffers]] [[nvim/nvim setup]] [[Linux/editor config]]

# vim config

> Startup settings in `.vimrc` / `init.vim` — indentation, search, syntax, and clipboard so Vim matches your project and OS.





## Interview Relevance
Ops and platform interviews care whether you can make stock Vim usable on a fresh box: tabs vs spaces, clipboard feature flags, and why `set clipboard=` silently fails.

## Sources
- [Vim help — options](https://vimhelp.org/options.txt.html) — deep-dive
- [Vim help — starting](https://vimhelp.org/starting.txt.html) — overview

## Core Definition
Vim reads user configuration on start (`~/.vimrc` or `$VIMINIT`). Options control editing behavior; feature flags at compile time (`+clipboard` vs `-clipboard`) decide what those options can do.

## Key Concepts
- **Compile features:** `vim --version | grep clipboard` — `-clipboard` means `set clipboard=unnamedplus` cannot work until you install a build with `+clipboard` (often `vim-gtk3` on Debian/Ubuntu).
- **Indentation triad:** `tabstop`, `shiftwidth`, `expandtab` → how Tab and `>>` behave; mismatch causes review noise.
- **Search UX:** `incsearch`, `ignorecase` + `smartcase` → type-as-you-find without losing case-sensitive searches for mixed-case patterns.
- **Filetype hooks:** `filetype indent on` → language-specific indent plugins; pair with project [[Linux/editor config|.editorconfig]] when teams share rules.

## Technical Details
```bash
vim --version | grep clipboard
# Need +clipboard (not -clipboard) for OS clipboard registers
sudo apt install vim-gtk3   # common fix on Debian/Ubuntu
```

```vim
" ~/.vimrc
set clipboard=unnamedplus
set expandtab
set shiftwidth=4
set tabstop=4
set autoindent
set smartindent
set incsearch
set ignorecase
set smartcase
syntax on
filetype plugin indent on
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Clipboard never syncs | `vim --version` shows `-clipboard` | Install GUI/featureful Vim; or use `xclip` + custom maps |
| Tabs still appear | `expandtab?` / `.editorconfig` | Align Vim options with editorconfig |
| Indent jumps oddly | `filetype indent` | Toggle or set per-filetype overrides |
| Configuration ignored | Wrong file (`init.vim` vs `.vimrc`) | Neovim uses `~/.config/nvim/init.vim` or `init.lua` — see [[nvim/nvim setup]] |

## Real-World Applications
Jump host with minimal Vim: drop a tiny `.vimrc` with `expandtab` / `shiftwidth` matching the repository, confirm `+clipboard` if you paste from the workstation.

## Pros/Cons or Trade-offs
- **Pro:** One file makes every new machine feel the same.
- **Con:** Heavy plugin stacks diverge from teammates’ stock Vim — keep server configs lean.

## Comparison
- vs Neovim `init.lua`: same ideas, Lua API and built-in LSP (see [[nvim/nvim setup]]).
- vs IDE settings sync: Vim configuration is plain text and SSH-friendly; no account required.

## Mistakes to Avoid
- Blaming `xclip` when the binary is `-clipboard` — the feature must be compiled in.
- Setting `tabstop=2` but `shiftwidth=4` — `>>` and Tab will disagree.
- Copying a huge plugin-manager configuration onto production bastions — prefer a minimal rc.
