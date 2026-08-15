[[vim commands]] [[vim keybindings]] [[vim buffers]]

# vim mark

> Named cursor bookmarks — jump back to a line or exact position inside a buffer or across files.

## Interview Relevance

Shows fluent multi-spot editing: set a mark at a call site, edit a definition elsewhere, jump back without search or mouse.

## Sources

- [Vim help — motion.txt (marks)](https://vimhelp.org/motion.txt.html#mark-motions) — deep-dive
- [Vim Tips Wiki — Using marks](https://vim.fandom.com/wiki/Using_marks) — overview

## Core Definition

A mark stores a cursor location. Lowercase marks are buffer-local; uppercase marks are global (file + position) and survive switching buffers.

## Key Concepts

- **Set / jump:** `m{a-zA-Z}` sets; `` `{char} `` jumps to exact position; `'{char}` jumps to first non-blank of that line.
- **Local vs global:** `a–z` per buffer; `A–Z` across files → use globals when bouncing between headers and sources.
- **Automatic marks:** `'[` / `']` last change; `'<` / `'>` last visual selection; `''` position before last jump → often enough without naming a letter.
- **Persistence:** uppercase marks can be saved in viminfo / shada → useful across sessions when configured.

## Technical Details

```vim
ma          " set mark a at cursor
'a          " jump to line of mark a
`a          " jump to exact row/column of mark a
:marks      " list marks
:delmarks a " delete mark a
:delmarks!  " delete all lowercase marks
```

| Mark | Scope | Typical use |
|------|-------|-------------|
| `a`–`z` | Current buffer | Temporary spots while editing one file |
| `A`–`Z` | Global (file) | Cross-file “come back here” |
| `0`–`9` | viminfo | Recent file positions (numbered) |
| `''` | Auto | Return after a jump |

## Real-World Applications

While reviewing a PR in Vim: `mA` on the failing test assertion, jump to implementation, fix, `` `A `` back to re-run the assertion mentally before writing.

## Pros/Cons or Trade-offs

- **Pro:** Instant random-access within a file without polluting the search history.
- **Con:** Easy to overwrite a mark; no UI unless you list `:marks`.

## Comparison

- vs Jumplist (`Ctrl-o`): jumplist is automatic history; marks are intentional bookmarks.
- vs [[vim buffers]] `:b`: buffers switch files; marks land on a precise spot inside a file.

## Mistakes to Avoid

- Using `'a` when you needed `` `a `` — you lose the column (annoying in long lines).
- Expecting lowercase marks to work after `:e otherfile` — they are buffer-local.
- Never listing `:marks` — silent overwrites make jumps feel “random.”
