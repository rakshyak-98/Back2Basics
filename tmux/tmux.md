- Session → multiple windows
- Window → full screen workspace
- Pane → splits inside window

```bash
tmux ls; // list session
tmux attach -t <name>; // attach previous session from outside of tmux
```

```bash
ctrl+b z; # Toggle focus on pane
ctrl+<space>; # Toggle pane layout
```

## Window

```text
C-b c // new window
C-b n // next window
C-b p // previous window
C-b <number> // jump to window
C-b , // rename window
C-b & // kill window
```

```text
C-b % // vertical split
C-b ****" // horizontal split
C-b o // switch pane
C-b x // kill pane
C-b z // zoom/unzoom pane
```

## Session

```text
C-b d // detach the current session
ctrl + b :
ctrl + b s // switch session
tmux switch-client -t <session-name>
rename-session my_session;
```

```bash
tmux rename-session -t 0 my_session_name
tmux new-session -d -s <session name>;

# Kill session
tmux ls | cut -d: -f1 | xargs -n1 tmux kill-session -t;
```

 **Loop to create multiple sessions**
```bash
port=5000

	for file in *.ts; do
    tmux new-session -d -s "stream_${port}" \
        "ffmpeg -re -stream_loop -1 -i '$file' -c copy -f mpegts udp://127.0.0.1:${port}?pkt_size=1316"

    ((port++))
done
```