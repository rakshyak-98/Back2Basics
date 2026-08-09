[[vim keybindings]] [[nvim setup]]

# commands

> commands — prepend method is used to add a new directory to the beginning of the runtime path.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** commands — plain job, how I run it, how I know it’s broken.


```bash
:Lazy update
:echo stdpath('config');
:echo stdpath('data'); #/usr/share directory
:message; # view the log file ~/.local/state/nvim.log
:lua =package.path; # print the current loaded path string
:options; # per instance options setup
```
```lua
print(vim.inspect(package.loaded['sg.nvim']));
```
```nvim
vim.opt.rtp:prepend(lazypath)
```
- `prepend` method is used to add a new directory to the beginning of the runtime path.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **commands** | Core idea of this note | “I can explain commands without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[vim keybindings]]] [[[nvim setup]]
