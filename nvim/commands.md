```shell
:Lazy update
:echo stdpath('config');
:echo stdpath('data'); #/usr/share directory
:message; # view the log file ~/.local/state/nvim.log
:lua =package.path; # print the current loaded path string
```

```lua
print(vim.inspect(package.loaded['sg.nvim']));
```

```nvim
vim.opt.rtp:prepend(lazypath)
```
- `prepend` method is used to add a new directory to the beginning of the runtime path.

> [!NOTE] `rtp` stands for runtime path. The runtime path is a list of directories that Neovim searches when looking for files, plugins and configurations.
- the runtime path determines where Neovim looks for its resources, such as plugins, syntax files, and other configuration files.