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
# - if you see -clipboard (a minux sign), your Vim is physically incapable of use `set clipboard`
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