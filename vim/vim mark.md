> [!INFO]
> The next time you want to edit your .vimrc, just press `'V` to open it. This assumes that you have kept the default ['viminfo'](http://vimdoc.sourceforge.net/cgi-bin/help?tag=%27viminfo%27) behavior, so that uppercase marks are all remembered in the [viminfo-file](http://vimdoc.sourceforge.net/cgi-bin/help?tag=viminfo-file) between Vim sessions.

| Command     | Description                                                       |
| ----------- | ----------------------------------------------------------------- |
| `ma`        | set mark **a** at current cursor location                         |
| `'a`        | jump to line of mark **a** (first non-blank character in line)    |
| `` `a ``    | jump to position (line and column) of mark **a**                  |
| `d'a`       | delete from current line to line of mark **a**                    |
| ``d`a``     | delete from current cursor position to position of mark **a**     |
| `c'a`       | change text from current line to line of mark **a**               |
| ``y`a``     | yank text to unnamed buffer from cursor to position of mark **a** |
| `:marks`    | list all the current marks                                        |
| `:marks aB` | list marks **a**, **B**<br>                                       |

| Command          | Description                                             |
| ---------------- | ------------------------------------------------------- |
| `:delmarks a`    | delete mark **a**                                       |
| `:delmarks a-d`  | delete marks **a**, **b**, **c**, **d**                 |
| `:delmarks abxy` | delete marks **a**, **b**, **x**, **y**                 |
| `:delmarks aA`   | delete marks **a**, **A**                               |
| `:delmarks!`     | delete all lowercase marks for the current buffer (a-z) |
