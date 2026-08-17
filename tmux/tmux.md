[[tmux copy-mode]] [[Linux/CLI]] [[Linux/Linux terminal]]

# tmux

> Terminal multiplexer — keep sessions alive, split panes, and reattach from another machine without killing processes.





## Interview Relevance
Interviewers (ops/SRE) expect session/window/pane model, detach/attach, and why tmux beats raw SSH for long jobs.

## Sources
- [tmux man page](https://man.openbsd.org/tmux) — deep-dive
- [Wikipedia — tmux](https://en.wikipedia.org/wiki/Tmux) — overview

## Key Concepts
- **Session:** detachable workspace attached to a server.
- **Window:** full-screen tabs inside a session.
- **Pane:** splits inside a window.
- **Prefix:** default `Ctrl-b` then a command key.

## Technical Details
```bash
tmux new -s work
tmux ls
tmux attach -t work
```

| Action | Keys / command |
|--------|----------------|
| Detach | `Ctrl-b d` |
| Zoom pane | `Ctrl-b z` |
| List sessions | `tmux ls` |

```
Session → Windows → Panes
```

## Real-World Applications
Start a deploy or `htop` in tmux, detach, reattach later from home over SSH.

**Example:** Laptop sleeps — SSH dies but the tmux session on the server keeps compilers running.

## Pros/Cons or Trade-offs
- **Pro:** Survives disconnects; scriptable layouts.
- **Con:** Nested tmux/SSH prefix collisions need remapping.

## Comparison
- vs screen: tmux is the modern default with better scripting/layouts.
- vs IDE terminals: tmux lives on the remote host, not only locally.

## Mistakes to Avoid
- Running `tmux` inside tmux without a clear outer prefix plan.
- Forgetting which session holds the prod shell.
- Leaving sensitive root sessions detached on shared bastions without locks.
