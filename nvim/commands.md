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

> [!NOTE] `rtp` stands for runtime path. The runtime path is a list of directories that Neovim searches when looking for files, plugins and configurations.
- the runtime path determines where Neovim looks for its resources, such as plugins, syntax files, and other configuration files.

### Treesitter
#### Error is decoration provider treesitter/highlighter.win
- indicates a problem with the query parsing, specifically related to an invalid node type.
```bash
:TSUpdate; # update the treesitter parsers
:TSInstall <language>; # check installed package
:checkhealth nvim-treesitter; # run healthcheck
```

## Telescope
### ignore files
```lua
require('telescope').setup{
    defaults = {
        file_ignore_patterns = { 'node_modules/', '.git/', '*.log', '*.tmp' },  -- Add patterns to ignore
        -- other default options can be added here
    },
    pickers = {
        find_files = {
            -- You can also override specific picker options here if needed
        },
    },
}
```