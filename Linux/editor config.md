[[terminal config]] [[Linux terminal]] [[gnome Colorschem]]

# editor config

> Editor configuration lives in dotfiles and LSP settings — align `EDITOR`, terminal capabilities, and language servers for consistent editing on servers and laptops.

## Environment

```bash
export EDITOR=vim
export VISUAL=vim
```

Many tools (`crontab -e`, `git commit`) honor `$EDITOR`.

## Vim / Neovim

```vim
" ~/.vimrc or ~/.config/nvim/init.lua
set number relativenumber
set expandtab shiftwidth=2 softtabstop=2
syntax on
```

## SSH remote editing

```bash
vim scp://user@host//etc/nginx/nginx.conf
# or local + rsync
```

## Related

[[terminal config]] · [[Scripting]]

## Sources

- `man 1 vim`
- [Neovim documentation](https://neov.io/doc/)
