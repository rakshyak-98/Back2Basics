[[vim keybindings]] [[vim buffers]] [[vim mark]] [[vim config]]

# vim commands

> Ex-mode and Normal-mode operations — edit, search, yank, and repeat without leaving the keyboard.

```txt
        vim commands ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Pairing sessions and on-call screens share Vim: can you jump, substitute gl…

## Sources
- [Vim help — usr_toc](https://vimhelp.org/usr_toc.txt.html) — overview
- [Vim help — change.txt](https://vimhelp.org/change.txt.html) — deep-dive
- [Vim Tips Wiki — Using marks](https://vim.fandom.com/wiki/Using_marks) — overview

## Key Concepts
- **Operator + motion:** `d` + `w`, `c` + `$`, `y` + `ip` → compose instead of memorizing one key per …
- **Ex ranges:** `:10,20s/foo/bar/g`, `:g/TODO/d` → batch edits across lines.
- **Registers:** `"ay` / `"ap` → named clipboards
- **Repeat:** `.` repeats last change; `@:` repeats last Ex command; macros with `q`.
- **Marks:** `ma` then `` `a `` — details in [[vim mark]].


- **Core:** Vim splits work into modes. Normal mode runs operators + motions

## Technical Details
```bash
vim -R file.txt          # read-only
```

```vim
:g/TODO/d                " delete lines matching TODO
Ctrl-a / Ctrl-x          " increment / decrement number under cursor
q:                       " command-line history window
@:                       " repeat last Ex command
"ay / "ap                " yank / paste register a
ma / 'a / `a             " set mark / line jump / exact jump
colorscheme habamax
```

| Task | Command |
|------|---------|
| Save / quit | `:w` `:q` `:wq` `:q!` |
| Search | `/pattern` `n` `N` |
| Global substitute | `:%s/old/new/gc` |
| Open alternate file | `:e#` or `Ctrl-^` |
| Show registers | `:reg` |
| Undo / redo | `u` `Ctrl-r` |

## Mistakes to Avoid
- **Mistake:** Running destructive `:g/.../d` without a dry visual check or und…
- **Mistake:** Assuming clipboard registers work on `-clipboard` builds
- **Mistake:** Confusing `'a` (line) with `` `a `` (exact position) when return…

## Pros/Cons or Trade-offs
- **Pro:** Composable grammar scales from one-char edits to macros.
- **Con:** Muscle memory takes time; wrong mode (`i` vs Normal) causes “Vim ate my keys” moments.

## Comparison
- vs [[vim keybindings]]: this note is the command catalog
- vs [[ed]]: Ex commands are the interactive, full-screen descendants of `ed`.


### Use cases
- Hotfix a configuration file under load: open read-only first (`vim -R`), conf…
