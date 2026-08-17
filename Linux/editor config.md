[[terminal config]] [[Linux terminal]] [[gnome Colorschem]] [[Scripting]]

# editor config

> Editor configuration lives in dotfiles and language-server settings — align `$EDITOR`, terminal capabilities, and keybindings so remote and local editing behave the same.





## Interview Relevance
Small but real ops signal: can you set `$EDITOR`/`$VISUAL`, survive `crontab -e` / `visudo` / `git commit`, and keep a minimal portable vimrc for jump boxes.

## Sources
- `man 1 vim` — overview
- [Neovim documentation](https://neovim.io/doc/) — deep-dive

## Core Definition
Tools that open an interactive editor honor `$EDITOR` (and often `$VISUAL`). Per-editor files (`~/.vimrc`, `~/.config/nvim/`) control tabs, syntax, and plugins; LSP settings add language intelligence on top.

## Key Concepts
- **EDITOR vs VISUAL:** Many programs prefer `VISUAL` for full-screen editors, `EDITOR` as fallback.
- **Dotfiles:** Portable vim/neovim config beats one-off machine tweaks.
- **Terminal capability:** Colors and keys depend on `$TERM` — [[terminal config]], [[Linux terminal]].
- **Remote edit:** scp-style paths, SSHFS, or local edit + sync.

## Technical Details
```bash
export EDITOR=vim
export VISUAL=vim
```

```vim
" ~/.vimrc or ~/.config/nvim/init.lua
set number relativenumber
set expandtab shiftwidth=2 softtabstop=2
syntax on
```

```bash
vim scp://user@host//etc/nginx/nginx.conf
```

## Real-World Applications
A new laptop exports `EDITOR=vim` in the shell profile so `kubectl edit`, `git commit`, and `visudo` all open the same editor with the same vimrc.

## Pros/Cons or Trade-offs
- **Pro:** One consistent editing model across servers and laptops.
- **Con:** Heavy IDE/LSP setups break on minimal bastion hosts — keep a lean fallback config.

## Comparison
vs [[terminal config]]: terminal sets colors/keys; editor config sets buffers and keybindings. vs GUI IDEs: CLI editors win on SSH and recovery TTYs; IDEs win for large refactors with project awareness.

## Mistakes to Avoid
- Leaving `$EDITOR` unset so cron/git open `nano` or fail in non-interactive contexts.
- Shipping a plugin-heavy neovim config to every production jump host.
- Forgetting that `sudoedit` / `sudo -e` may not load your user vimrc the way you expect — know the path.
