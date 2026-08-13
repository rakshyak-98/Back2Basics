[[netrw file explorer]] [[vim keybindings]] [[Linux/CLI]]

# Vim buffers

> In-memory views of files — switch, list, and close without quitting Vim.

---

## How it works


```
:edit a.txt  → buffer #1
:edit b.txt  → buffer #2 (a hidden unless hiddenunload)
:split c.txt → buffer #3, two windows
```


## Configuration and commands

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


## When things break

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


## When not to use

- Don't `:bd!` everything to "clean up" during a refactor — use `:tab`/`session` workflow instead.
- Don't rely on buffer numbers across sessions — they reset.


## Related

[[netrw file explorer]] [[Linux/CLI]] [[editor configuration]]

## Sources

- [Wikipedia — vim buffers](https://en.wikipedia.org/wiki/vim_buffers)
