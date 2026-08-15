[[netrw file explorer]] [[vim keybindings]] [[vim commands]] [[Linux/editor config]]

# vim buffers

> In-memory file views in Vim — list, switch, and close them without quitting the editor.

## Interview Relevance

Editors ask how you juggle multiple files under SSH: buffers vs windows vs tabs. Correct answer: buffer = file content; window = viewport; tab = window layout.

## Sources

- [Vim help — windows and buffers](https://vimhelp.org/windows.txt.html) — deep-dive
- [Vim Tips Wiki — buffers](https://vim.fandom.com/wiki/Buffers) — overview

## Core Definition

A buffer holds the text of a file (or unnamed scratch). Multiple windows can show the same buffer; closing a window does not always delete the buffer.

## Key Concepts

- **Buffer vs window vs tab:** buffer = data; window = view; tab page = arrangement of windows → saying “close the tab” ≠ “unload the file.”
- **`hidden`:** with `set hidden`, you can leave a modified buffer without writing → essential for fluid multi-file editing.
- **Listed vs unlisted:** `:ls` shows listed buffers; help/quickfix may be unlisted → don’t panic when counts look odd.
- **Modified flag:** `:bd` refuses dirty buffers unless `!` or you write first → protects unsaved work.

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

## Real-World Applications

Debugging across service + configuration + test file in one Vim session on a jump host — cycle with `:bn` / `:b name` instead of reopening paths.

## Pros/Cons or Trade-offs

- **Pro:** Fast multi-file workflow with one process and shared registers/marks.
- **Con:** Buffer numbers reset across sessions — don’t script hard-coded numbers.

## Comparison

- vs Windows (`:split`): windows display buffers; many windows can share one buffer.
- vs Tabs: tabs organize window layouts, not “one file each” (common misconception).

## Mistakes to Avoid

- Treating `:bd` as “close window” — the window may stay empty until you open another file.
- `:bd!` on a terminal buffer — may kill a running job.
- Mass `:bd!` mid-refactor — prefer sessions / tabs when you still need those files.
