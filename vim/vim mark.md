[[Vim CLI]] [[vim keybindings]] [[vim buffers]]

# vim mark

> Named cursor bookmarks — jump back to a line or exact position inside a buffer or across files.

```txt
        vim mark ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows fluent multi-spot editing: set a mark at a call site, edit a definition…

## Sources
- [Vim help — motion.txt (marks)](https://vimhelp.org/motion.txt.html#mark-motions) — deep-dive
- [Vim Tips Wiki — Using marks](https://vim.fandom.com/wiki/Using_marks) — overview

## Key Concepts
- **Set / jump:** `m{a-zA-Z}` sets
- **Local vs global:** `a–z` per buffer
- **Automatic marks:** `'[` / `']` last change
- **Persistence:** uppercase marks can be saved in viminfo / shada → useful across sessions when…


- **Core:** A mark stores a cursor location. Lowercase marks are buffer-local

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

## Mistakes to Avoid
- **Mistake:** Using `'a` when you needed `` `a ``
- **Mistake:** Expecting lowercase marks to work after `:e otherfile`
- **Mistake:** Never listing `:marks`

## Pros/Cons or Trade-offs
- **Pro:** Instant random-access within a file without polluting the search history.
- **Con:** Easy to overwrite a mark; no UI unless you list `:marks`.

## Comparison
- vs Jumplist (`Ctrl-o`): jumplist is automatic history; marks are intentional bookmarks.
- vs [[vim buffers]] `:b`: buffers switch files; marks land on a precise spot inside a file.


### Use cases
- While reviewing a PR in Vim: `mA` on the failing test assertion, jump to impl…
