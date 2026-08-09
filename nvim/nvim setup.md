[[vim keybindings]] [[Descriptive/LSP]]

# nvim setup

> nvim setup — short field notes on what it is and how to use it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** nvim setup — plain job, how I run it, how I know it’s broken.


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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **nvim setup** | Core idea of this note | “I can explain nvim setup without jargon.” |
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

[[vim keybindings]]] [[[Descriptive/LSP]]
