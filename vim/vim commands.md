[[vim keybindings]] [[vim buffers]]

# vim commands

> vim commands — ctrl-a (increment number under cursor)

---

## Mental model

**Say it in one breath:** vim commands — ctrl-a (increment number under cursor)

```bash
vim -R ; # start vim in Read-only mode.
```
```bash
:g/TODO/d; # delete all lines containing work TODO
```
```vim
Ctrl-a (increment number under cursor)
Ctrl-x (decrement number under cursor)
```
```vim
q: (open command history)
@: (repeat last command)
```
### yank
```vim
"ay (yank into register 'a')
"ap (paste from register 'a')
```
### mark
 [mark document](https://vim.fandom.com/wiki/Using_marks)
```vim
ma (set mark 'a')
'a (jump to line of mark 'a')
`a (jump to exact position of mark 'a')
```
```vim
m{char}
```
`{char}` = a-z (buffer local), A-Z (global)
### Vim rc file
```vim
colorscheme habamax
```
### Enable system clipboard


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[vim keybindings]]] [[[vim buffers]]
