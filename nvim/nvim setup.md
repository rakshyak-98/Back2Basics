[[commands]] [[Descriptive/LSP]] [[Descriptive/vscode]]

# Neovim setup

> Bootstrap config (Lua today) — options, plugin manager, LSP, treesitter, and keymaps so Neovim feels like a modern IDE.

## Interview Relevance

DX discussions: Lua config vs vimscript, LSP client built-in, and keeping a portable dotfiles repo.

## Sources

- [Neovim — Lua guide](https://neovim.io/doc/user/lua-guide.html) — deep-dive
- [Neovim — LSP](https://neovim.io/doc/user/lsp.html) — overview

## Key Concepts

- **Config path:** `~/.config/nvim/init.lua` (and Lua modules).
- **Plugin manager:** lazy.nvim / packer-era tools → declare plugins.
- **LSP:** `vim.lsp` + language servers for completion/diagnostics.
- **Treesitter:** better syntax/ast motions.
- **Portable dots:** symlink via git.

## Technical Details

Minimal skeleton ideas:

```lua
vim.opt.number = true
vim.opt.relativenumber = true
vim.g.mapleader = " "
-- plugin manager bootstrap + lspconfig + treesitter
```

| Layer | Role |
|-------|------|
| Options | Editor behavior |
| Keymaps | Leader shortcuts |
| Plugins | Fuzzy find, git, UI |
| LSP | Language intelligence |

## Real-World Applications

Engineers keep one Neovim config across machines; CI bastions get a thin config without heavy GUI plugins.

**Example:** New laptop — clone dotfiles, install language servers with mason.nvim or system packages.

## Pros/Cons or Trade-offs

- **Pro:** Extremely customizable; works over SSH.
- **Con:** You own breakage when plugins conflict.

## Comparison

- vs VS Code: more DIY; similar LSP outcomes when configured.
- vs stock Vim: Neovim adds Lua and first-class LSP client APIs.

## Mistakes to Avoid

- Copying a huge config you do not understand.
- Blocking UI with sync plugin loads — prefer lazy loading.
- Mixing vimscript and Lua randomly without structure.
