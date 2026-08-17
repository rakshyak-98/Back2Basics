[[netrw file explorer]] [[vim keybindings]] [[vim commands]] [[Linux/editor config]]

# vim buffers

> In-memory file views in Vim — list, switch, and close them without quitting the editor.

```txt
        vim buffers ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Editors ask how you juggle multiple files under SSH: buffers vs windows vs ta…

## Sources
- [Vim help — windows and buffers](https://vimhelp.org/windows.txt.html) — deep-dive
- [Vim Tips Wiki — buffers](https://vim.fandom.com/wiki/Buffers) — overview

## Key Concepts
- **Buffer vs window vs tab:** buffer = data
- **`hidden`:** with `set hidden`, you can leave a modified buffer without writing → essentia…
- **Listed vs unlisted:** `:ls` shows listed buffers
- **Modified flag:** `:bd` refuses dirty buffers unless `!` or you write first → protects unsaved …


- **Core:** A buffer holds the text of a file (or unnamed scratch). Multiple windows can …

## Technical Details
```
:edit a.txt  → buffer #1
:edit b.txt  → buffer #2 (a may stay loaded if hidden)
:split c.txt → buffer #3, two windows
```

```vim
:ls                   " list buffers
:b 2                  " switch by number
:b filename           " match by name
:bn / :bp             " next / previous
:bd                   " delete buffer (fails if unsaved)
:bd!                  " force delete
:only                 " close other windows; buffers remain
set hidden            " allow switching away from unsaved buffers
nnoremap <leader>b :ls<CR>:b
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t switch (unsaved) | `:set hidden?` | `:set hidden` or `:w` first |
| `:bd` refuses | Modified flag | `:w` or `:bd!` |
| Huge buffer list | `:ls` | `:bd` unused; avoid blind `:bufdo bd` |
| Wrong file after `:b` | Ambiguous match | Prefer number or unique substring |

## Mistakes to Avoid
- **Mistake:** Treating `:bd` as “close window”
- **Mistake:** `:bd!` on a terminal buffer — may kill a running job
- **Mistake:** Mass `:bd!` mid-refactor

## Pros/Cons or Trade-offs
- **Pro:** Fast multi-file workflow with one process and shared registers/marks.
- **Con:** Buffer numbers reset across sessions — don’t script hard-coded numbers.

## Comparison
- vs Windows (`:split`): windows display buffers; many windows can share one buffer.
- vs Tabs: tabs organize window layouts, not “one file each” (common misconception).


### Use cases
- Debugging across service + configuration + test file in one Vim session on a …
