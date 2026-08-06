[[vim buffers]] [[Descriptive/LSP]] [[nvim setup]] [[zed keybindings]]

# Vim / Neovim keybindings — go to

> LSP-powered navigation (definition, references, implementation) plus jump-back — requires Neovim with a language server attached; plain Vim needs ctags or a plugin.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Go to (Neovim 0.11+ defaults)]]
- [[#Go to (on LSP attach — buffer-local)]]
- [[#Common manual mappings (`gd` style)]]
- [[#Jump back after go to]]
- [[#Without LSP (plain Vim / fallback)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Go to** commands ask the [[Descriptive/LSP|LSP]] (or ctags) where a symbol lives, then jump the cursor there. Neovim 0.11+ ships **global** `gr*` maps at startup; **buffer-local** maps (`K`, `CTRL-]`, diagnostics) apply when an LSP client attaches.

After any jump, use the **jumplist** (`Ctrl-o` / `Ctrl-i`) or **tag stack** (`Ctrl-t`) to return — LSP single-result jumps push onto the tag stack.

```
cursor on symbol → go-to key → LSP query → jump (or quickfix list)
                                    ↓
                              Ctrl-o to jump back
```

See [[Descriptive/LSP#Difference between Go to Reference, Definition, Implementation]] for when to use each target.

## Standard config / commands

…

## Go to (Neovim 0.11+ defaults)

These are created **unconditionally** when Nvim starts (your own maps override them):

| Action                     | Key     | LSP call                        |
| -------------------------- | ------- | ------------------------------- |
| Go to references           | `g r r` | `vim.lsp.buf.references()`      |
| Go to implementation       | `g r i` | `vim.lsp.buf.implementation()`  |
| Go to type definition      | `g r t` | `vim.lsp.buf.type_definition()` |
| Rename symbol              | `g r n` | `vim.lsp.buf.rename()`          |
| Code action                | `g r a` | `vim.lsp.buf.code_action()`     |
| Run codelens               | `g r x` | `vim.lsp.codelens.run()`        |
| Document symbols (outline) | `g O`   | `vim.lsp.buf.document_symbol()` |

## Go to (on LSP attach — buffer-local)

Set when a language server attaches and you have not overridden them:

| Action | Key | Notes |
|--------|-----|-------|
| Go to definition | `Ctrl-]` | Uses `tagfunc` → LSP `textDocument/definition`; falls back to tags |
| Definition in split | `Ctrl-W` `]` | Same, horizontal split |
| Definition in split (alt) | `Ctrl-W` `}` | Vertical split variant |
| Hover / docs | `K` | Float window; `K` `K` focuses it |
| Signature help | `Ctrl-s` (insert) | Parameter hints while typing |
| Next diagnostic | `] d` | Same-buffer diagnostic |
| Previous diagnostic | `[ d` | Same-buffer diagnostic |
| First diagnostic | `[ D` | Jump to first |
| Last diagnostic | `] D` | Jump to last |

`:tjump` / `Ctrl-]` also respect LSP when `tagfunc` is active.

## Common manual mappings (`gd` style)

Neovim does **not** default `gd` / `gD`. Many configs add these in `LspAttach`:

| Action | Typical key | LSP call |
|--------|-------------|----------|
| Go to definition | `g d` | `vim.lsp.buf.definition()` |
| Go to declaration | `g D` | `vim.lsp.buf.declaration()` |
| Go to references | `g r` | `vim.lsp.buf.references()` — conflicts with `grr` prefix on 0.11+ |
| Go to implementation | `g i` | `vim.lsp.buf.implementation()` |
| Go to type definition | `g t` | `vim.lsp.buf.type_definition()` |

Example for `init.lua` / `LspAttach`:

```lua
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(ev)
    local map = function(mode, lhs, rhs)
      vim.keymap.set(mode, lhs, rhs, { buffer = ev.buf, silent = true })
    end
    map('n', 'gd', vim.lsp.buf.definition)
    map('n', 'gD', vim.lsp.buf.declaration)
    map('n', 'gr', vim.lsp.buf.references)
    map('n', 'gi', vim.lsp.buf.implementation)
    map('n', 'gt', vim.lsp.buf.type_definition)
  end,
})
```

## Jump back after go to

| Action | Key |
|--------|-----|
| Older position (jumplist) | `Ctrl-o` |
| Newer position (jumplist) | `Ctrl-i` |
| Pop tag stack (after `Ctrl-]` / single-result LSP jump) | `Ctrl-t` |
| List jump locations | `:jumps` |

## Without LSP (plain Vim / fallback)

| Action | Key / command |
|--------|----------------|
| Jump to tag (ctags) | `Ctrl-]` on symbol with tags file |
| Tag list if ambiguous | `:tselect` / `:tjump` |
| Generate tags | `ctags -R .` then `:set tags=./tags;,tags` |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `grr` / `gd` does nothing | `:LspInfo` or `:checkhealth vim.lsp` | Start language server; open project root with `root_markers` |
| Goes to wrong file | Multiple workspaces / stale build | Regenerate `compile_commands.json`; restart LSP |
| Quickfix list instead of jump | Multiple results | Pick entry; or map with `{ jump = true }` in handler opts |
| `Ctrl-]` uses tags not LSP | `:set tagfunc?` | Ensure LSP attached; `tagfunc` should be `v:lua.vim.lsp.tagfunc` |
| `K` opens man page | Custom `K` map or `keywordprg` | Remove override; LSP sets hover on attach |
| Can't jump back | Used `Ctrl-o` from insert | `Esc` first; try `Ctrl-t` if LSP used tag stack |

## Gotchas

> [!WARNING]
> **`gr` vs `grr`** — On 0.11+, `g` then `r` starts the `gr*` chord; `gd`-style `gr` for references needs an explicit map (see above).
>
> **LSP must be running** — Go-to is a no-op (or tag-only) without an attached client for that buffer's filetype.
>
> **Declaration** — Many servers omit `textDocument/declaration`; use definition instead.

## When NOT to use

…

## Related

[[vim buffers]] [[vim mark]] [[Descriptive/LSP]] [[nvim setup]] [[nvim/commands]] [[zed keybindings]]
