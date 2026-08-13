[[vim keybindings]] [[Descriptive/LSP]]

# nvim setup

> nvim setup — short field notes on what it is and how to use it.

---

## How it works

```bash
apt update neovim;
nvim --version;
```
install `lazy.nvim` plugin manager
```bash
git clone https://github.com/folke/lazy.nvim.git \
~/.local/share/nvim/lazy/lazy.nvim
```
Create configuration directory
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


---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Steps

1. …


## Verification

```bash
# smoke test
```


## Related

[[vim keybindings]]] [[[Descriptive/LSP]]

## Sources

- [Wikipedia — nvim setup](https://en.wikipedia.org/wiki/nvim_setup)
