```bash
vim -R ; # start vim in Read-only mode.
```

```bash
:g/TODO/d; # delete all lines containing work TODO
```

```vim
Ctrl-a (increment number under cursor)
Ctrl-x (decrement number under cursor)
```

```vim
q: (open command history)
@: (repeat last command)
```

### yank
```vim
"ay (yank into register 'a')
"ap (paste from register 'a')
```

### mark
 
 [mark doc](https://vim.fandom.com/wiki/Using_marks)

```vim
ma (set mark 'a')
'a (jump to line of mark 'a')
`a (jump to exact position of mark 'a')
```

```vim
m{char}
```
`{char}` = a-z (buffer local), A-Z (global)

### Vim rc file
```vim
colorscheme habamax
```

### Enable system clipboard

> [!INFO] 
> if you see `+clipboard` clipboard is supported
> if you see `-clipboard` clipboard is not supported
```bash
vim --version | grep clipboard; 
```

```bash
sudo apt install vim-gtk3; # install vim with clipboard support
```

```vim
"+y        " Yank to system clipboard
"+p        " Paste from system clipboard
```

#### Make clipboard default
> [!INFO]
> uses the `+` register (system clipboard) for all the yank/paste.
```vim
set clipboard=unnamedplus;
```