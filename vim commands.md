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