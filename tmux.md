```bash
tmux ls; // list session
tmux attach -t <name>; // attach previous session
```

## Window

```text
C-b d // detach the current session
C-b c // new window
C-b n // next window
C-b p // previous window
C-b <number> // jump to window
C-b , // rename window
C-b & // kill window
```

```text
C-b % // vertical split
C-b " // horizontal split
C-b o // switch pane
C-b x // kill pane
C-b z // zoom/unzoom pane
```

## Session

```text
ctrl + b :
rename-session my_session;
```

```bash
tmux rename-session -t 0 my_session_name
```