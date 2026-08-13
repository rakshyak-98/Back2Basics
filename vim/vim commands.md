[[vim keybindings]] [[vim buffers]]

# vim commands

> vim commands — ctrl-a (increment number under cursor)

---

## How it works

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


## Quick reference

| Task | Command |
|------|---------|
| … | `…` |


## Configuration and commands

```bash
# version + config path
# dry-run when available
```

---


## Options and flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |


## Examples

```bash
# …
```


## When things break

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


## When not to use

- Avoid the tool if a simpler built-in covers the job.

---


## Related

[[vim keybindings]]] [[[vim buffers]]

## Sources

- [Wikipedia — vim commands](https://en.wikipedia.org/wiki/vim_commands)
