[[vim buffers]] [[Vim CLI]] [[vim mark]] [[Descriptive/LSP]] [[nvim/nvim setup]]

# vim keybindings

> Keyboard maps for modes and navigation — move, jump to definitions, and return via jumplist / tag stack.

```txt
        vim keybindings ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Signals you can navigate a large codebase in Vim/Neovim under screen share: m…

## Sources
- [Neovim — LSP defaults](https://neovim.io/doc/user/lsp.html) — deep-dive
- [Vim help — map.txt](https://vimhelp.org/map.txt.html) — deep-dive
- [Vim help — motion.txt](https://vimhelp.org/motion.txt.html) — overview

## Key Concepts
- **Modes:** Normal for verbs, Insert for typing, Visual for selections, Ex (`:`) for comm…
- **Motions vs operators:** `w` / `}` / `gg` move; `d` / `c` / `y` act
- **LSP go-to:** definition, references, implementation
- **Jumplist / tag stack:** `Ctrl-o` / `Ctrl-i` walk jump history
- **Custom maps:** `nnoremap` (non-recursive Normal) preferred over `nmap` to avoid remap loops.


- **Core:** Keybindings are Normal/Visual/Insert maps plus built-in motions. In Neovim, l…

## Technical Details
```
cursor on symbol → go-to key → LSP query → jump (or quickfix)
                                    ↓
                              Ctrl-o / Ctrl-t to return
```

- Typical Neovim LSP maps (0.11+ ships many `gr*` defaults

| Action | Common map |
|--------|------------|
| Hover | `K` |
| Definition | `gd` / `CTRL-]` |
| References | `grr` (Neovim default) |
| Implementation | `gri` |
| Signature help | `CTRL-s` (when mapped) |
| Jump back | `Ctrl-o` or `Ctrl-t` |

```vim
" Example custom maps (Vim + ctags, or older Neovim)
nnoremap gd <Cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <leader>rn <Cmd>lua vim.lsp.buf.rename()<CR>
```

- Plain Vim without LSP: `ctags -R` then `Ctrl-]` / `Ctrl-t`, or a plugin.

| Symptom | Check | Fix |
|---------|-------|-----|
| Go-to does nothing | LSP attached? `:LspInfo` | Start language server; open correct root |
| Jump but can’t return | Used mouse / new edit | Prefer `Ctrl-o`; check `:jumps` |
| Map inserts literal keys | Wrong mode / recursive map | Use `nnoremap`; verify mode |
| Works in Neovim only | Feature not in Vim | Install LSP plugin or use ctags |

## Mistakes to Avoid
- **Mistake:** Remapping without `noremap` — recursive maps surprise you later
- **Mistake:** Expecting LSP maps in stock Vim
- **Mistake:** Ignoring jumplist after deep dives

## Pros/Cons or Trade-offs
- **Pro:** Hands stay on home row; navigation scales with LSP.
- **Con:** Maps differ across Vim vs Neovim versions — document team defaults.

## Comparison
- vs IDE F12 / Cmd-click: same idea; Vim exposes jumplist explicitly.
- vs [[zed/zed keybindings]]: different editor, same “go to definition + back” mental model.


### Use cases
- Live debugging a service: `gd` into a handler, chase one more definition, the…
