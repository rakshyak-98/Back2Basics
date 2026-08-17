[[tmux copy-mode]] [[Linux/CLI]] [[Linux/Linux terminal]]

# tmux

> Terminal multiplexer — keep sessions alive, split panes, and reattach from another machine without killing processes.

```txt
        tmux ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers (ops/SRE) expect session/window/pane model, detach/attach, and w…

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

## Mistakes to Avoid
- **Mistake:** Running `tmux` inside tmux without a clear outer prefix plan
- **Mistake:** Forgetting which session holds the prod shell
- **Mistake:** Leaving sensitive root sessions detached on shared bastions with…

## Pros/Cons or Trade-offs
- **Pro:** Survives disconnects; scriptable layouts.
- **Con:** Nested tmux/SSH prefix collisions need remapping.

## Comparison
- vs screen: tmux is the modern default with better scripting/layouts.
- vs IDE terminals: tmux lives on the remote host, not only locally.


### Use cases
- Start a deploy or `htop` in tmux, detach, reattach later from home over SSH.

- **Example:** Laptop sleeps
