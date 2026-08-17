[[vim keybindings]] [[vim buffers]] [[vim mark]] [[vim config]]

# vim commands

> Ex-mode and Normal-mode operations — edit, search, yank, and repeat without leaving the keyboard.





## Interview Relevance
Pairing interviews and on-call screens share Vim: can you jump, substitute globally, use registers, and recover from mistakes? Commands beat mouse navigation under time pressure.

## Sources
- [Vim help — usr_toc](https://vimhelp.org/usr_toc.txt.html) — overview
- [Vim help — change.txt](https://vimhelp.org/change.txt.html) — deep-dive
- [Vim Tips Wiki — Using marks](https://vim.fandom.com/wiki/Using_marks) — overview

## Core Definition
Vim splits work into modes. Normal mode runs operators + motions; `:` enters Ex commands (line ranges, global ops, writes). Registers and marks extend that model for multi-spot edits.

## Key Concepts
- **Operator + motion:** `d` + `w`, `c` + `$`, `y` + `ip` → compose instead of memorizing one key per action.
- **Ex ranges:** `:10,20s/foo/bar/g`, `:g/TODO/d` → batch edits across lines.
- **Registers:** `"ay` / `"ap` → named clipboards; `"+` / `"*` for system clipboard when compiled in (see [[vim config]]).
- **Repeat:** `.` repeats last change; `@:` repeats last Ex command; macros with `q`.
- **Marks:** `ma` then `` `a `` — details in [[vim mark]].

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

## Real-World Applications
Hotfix a configuration file under load: open read-only first (`vim -R`), confirm the bad value, re-open writable, `:%s/.../.../`, write, reload the service.

## Pros/Cons or Trade-offs
- **Pro:** Composable grammar scales from one-char edits to macros.
- **Con:** Muscle memory takes time; wrong mode (`i` vs Normal) causes “Vim ate my keys” moments.

## Comparison
- vs [[vim keybindings]]: this note is the command catalog; keybindings focus on navigation / LSP jumps.
- vs [[ed]]: Ex commands are the interactive, full-screen descendants of `ed`.

## Mistakes to Avoid
- Running destructive `:g/.../d` without a dry visual check or undo plan.
- Assuming clipboard registers work on `-clipboard` builds — verify with `vim --version`.
- Confusing `'a` (line) with `` `a `` (exact position) when returning to a mark.
