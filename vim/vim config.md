[[vim]]

# - if you see -clipboard (a minux sign), your Vim is physically incapable of use `set clipboard`

> - if you see -clipboard (a minux sign), your Vim is physically incapable of use `set clipboard` — set shiftwidth=4 # indentation commands >>, << shift by 4

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** - if you see -clipboard (a minux sign), your Vim is physically incapable of use `set clipboard` — set shiftwidth=4 # indentation commands >>, << shift by 4

```bash
```
```bash
set clipboard=unnamedplus
set expandtab
set shiftwidth=4 # indentation commands >>, << shift by 4 spaces.
set tabstop=4 # pressing <Tab> inserts 2 spaces because of expandtab.
set expandtab # tabs are converted to spaces.
```
- Even with `xclip` installed, there is one major thing you have to check
`+clipboard` check
```bash
vim --version | grep clipboard;
```
- fix you need to install the enhanced version of vim
```bash
sudo apt install vim-gtk3; # this provide the liberary hooks for xclip
```
```bash
set autoindent
set smartindent
set clipboard=unnamedplus
set shiftwidth=4
set tabstop=4
set expandtab
set incsearch
set ignorecase
set smartcase
syntax on
filetype indent on
```


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[vim]]
