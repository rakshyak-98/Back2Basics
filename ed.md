
| Command      | Description           |
| ------------ | --------------------- |
| `e filename` | Open file for editing |
| `w`          | Write changes to file |
| `w filename` | Write to new file     |
| `q`          | Quit                  |
| `q!`         | Quit without saving   |

| Command | Description                  |
| ------- | ---------------------------- |
| `1`     | Go to first line             |
| `$`     | Go to last line              |
| `.`     | Current line                 |
| `n`     | Show line number and content |

| Command | Description                            |
| ------- | -------------------------------------- |
| `a`     | Append after current line (`.` to end) |
| `i`     | Insert before current line             |
| `c`     | Change current line                    |
| `.`     | End input mode                         |

| Command | Description         |
| ------- | ------------------- |
| `d`     | Delete current line |
| `N,Md`  | Delete lines N to M |

| Command             | Description                           |
| ------------------- | ------------------------------------- |
| `s/old/new/`        | Replace first match in current line   |
| `s/old/new/g`       | Replace all matches in current line   |
| `N,Ms/old/new/g`    | Replace in range N to M               |

| Command    | Description        |
| ---------- | ------------------ |
| `/pattern` | Search forward     |
| `?pattern` | Search backward    |
| `n`        | Repeat last search |

| Command | Description             |
| ------- | ----------------------- |
| `p`     | Print current line      |
| `N,Mp`  | Print lines N to M      |
| `n`     | Print with line numbers |


```bash
> ed myfile.txt
1    # go to first line
a    # append lines
hello
world
.    # finish input
1s/hello/hi/    # replace in line 1
w               # save file
q               # quit

```
