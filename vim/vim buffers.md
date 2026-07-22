[[netrw file explorer]] [[Linux/CLI]]

# Vim buffers

> In-memory views of files — switch, list, and close without quitting Vim.

## Mental model

Opening a file loads a **buffer** (text + metadata). Buffers can be hidden (not shown in a window) or active (displayed). Windows are views onto buffers; one buffer can appear in multiple windows. Unsaved changes live in the buffer until `:w` or `:wa`.

```
:edit a.txt  → buffer #1
:edit b.txt  → buffer #2 (a hidden unless hiddenunload)
:split c.txt → buffer #3, two windows
```

## Standard config / commands

```vim
:ls                   " list buffers (+ hidden)
:b 2                  " switch to buffer 2
:b filename           " fuzzy by name
:bn / :bp             " next / previous
:bd                   " delete buffer (fail if unsaved)
:bd!                  " force delete
:bn!                  " next even with unsaved (if hidden allowed)
:only                 " close other windows, keep buffer
```

### Keep hidden buffers

```vim
set hidden              " switch away from unsaved buffer
```

### Quick buffer cycle

```vim
nnoremap <leader>b :ls<CR>:b
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can't switch buffer (unsaved) | `:set hidden?` | `:set hidden` or `:w` first |
| `:bd` refuses | Modified flag | `:w` or `:bd!` |
| Buffer list huge | `:ls` | `:bd` unused; `:bufdo bd` (careful) |
| Wrong file after `:b` | Multiple matches | Use full path `:b %` or buffer number |
| Changes lost | `:q!` vs `:bd!` | `:wa` habit before mass `:bd` |

## Gotchas

> [!WARNING]
> **`:bd` closes buffer, not window** — layout can look empty until you open another file.
>
> **Terminal buffer** — special type; `:bd` may kill running process.
>
> **Auto-save plugins** — race with manual `:bd!` expectations.

## When NOT to use

- Don't `:bd!` everything to "clean up" during a refactor — use `:tab`/`session` workflow instead.
- Don't rely on buffer numbers across sessions — they reset.

## Related

[[netrw file explorer]] [[Linux/CLI]] [[editor config]]
