[[commands]] [[Descriptive/LSP]] [[Descriptive/vscode]]

# Neovim setup

> Bootstrap config (Lua today) — options, plugin manager, LSP, treesitter, and keymaps so Neovim feels like a modern IDE.

```txt
        Neovim setup ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** DX discussions: Lua config vs vimscript, LSP client built-in, and keeping a p…

## Sources
- [Neovim — Lua guide](https://neovim.io/doc/user/lua-guide.html) — deep-dive
- [Neovim — LSP](https://neovim.io/doc/user/lsp.html) — overview

## Technical Details
- Minimal skeleton ideas:

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

## Mistakes to Avoid
- **Mistake:** Copying a huge config you do not understand
- **Mistake:** Blocking UI with sync plugin loads — prefer lazy loading
- **Mistake:** Mixing vimscript and Lua randomly without structure

## Pros/Cons or Trade-offs
- **Pro:** Extremely customizable; works over SSH.
- **Con:** You own breakage when plugins conflict.

## Comparison
- vs VS Code: more DIY; similar LSP outcomes when configured.
- vs stock Vim: Neovim adds Lua and first-class LSP client APIs.


### Use cases
- Engineers keep one Neovim config across machines

- **Example:** New laptop
