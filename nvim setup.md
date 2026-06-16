```bash
apt update neovim;
nvim --version;
```

install `lazy.nvim` plugin manager

```bash
git clone https://github.com/folke/lazy.nvim.git \  
~/.local/share/nvim/lazy/lazy.nvim
```

Create config directory

```bash
mkdir -p ~/.config/nvim/lua/plugins
```

```lua ~/.config/nvim/init.lua

vim.opt.rtp:prepend(vim.fn.stdpath("data") .. "/lazy/lazy.nvim")

require("lazy").setup({
  {
    "ldelossa/nvim-ide",
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    config = function()
      require("ide-config")
    end,
  },
})
```
