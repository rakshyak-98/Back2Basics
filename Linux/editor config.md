[[terminal config]] [[Linux terminal]] [[gnome Colorschem]] [[Scripting]]

# editor config

> Editor configuration lives in dotfiles and language-server settings — align `$EDITOR`, terminal capabilities, and keybindings so remote and local editing behave the same.

```txt
        editor config ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Small but real ops signal: can you set `$EDITOR`/`$VISUAL`, survive `crontab …

## Sources
- `man 1 vim` — overview
- [Neovim documentation](https://neovim.io/doc/) — deep-dive

## Key Concepts
- **EDITOR vs VISUAL:** Many programs prefer `VISUAL` for full-screen editors, `EDITOR` as fallback.
- **Dotfiles:** Portable vim/neovim config beats one-off machine tweaks.
- **Terminal capability:** Colors and keys depend on `$TERM` — [[terminal config]], [[Linux terminal]].
- **Remote edit:** scp-style paths, SSHFS, or local edit + sync.


- **Core:** Tools that open an interactive editor honor `$EDITOR` (and often `$VISUAL`). …

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

## Mistakes to Avoid
- **Mistake:** Leaving `$EDITOR` unset so cron/git open `nano` or fail in non-i…
- **Mistake:** Shipping a plugin-heavy neovim config to every production jump h…
- **Mistake:** Forgetting that `sudoedit` / `sudo -e` may not load your user vi…

## Pros/Cons or Trade-offs
- **Pro:** One consistent editing model across servers and laptops.
- **Con:** Heavy IDE/LSP setups break on minimal bastion hosts — keep a lean fallback config.

## Comparison
- vs [[terminal config]]: terminal sets colors/keys


### Use cases
- A new laptop exports `EDITOR=vim` in the shell profile so `kubectl edit`, `gi…
