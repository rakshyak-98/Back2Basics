[[vim keybindings]] [[nvim setup]]

# commands

> commands — prepend method is used to add a new directory to the beginning of the runtime path.

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

## Related

[[vim keybindings]]] [[[nvim setup]]
