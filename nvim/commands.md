[[vim keybindings]] [[nvim setup]]

# commands

> commands — prepend method is used to add a new directory to the beginning of the runtime path.

---

## Index

- [[#Quick reference]]
- [[#Common commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Common commands

```bash
# …
```

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

**Say it in one breath:** commands — prepend method is used to add a new directory to the beginning of the runtime path.

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


---

## Examples

```bash
# …
```

## Related

[[vim keybindings]]] [[[nvim setup]]
