[[tmux]]

# tmux

> tmux — window → full screen workspace

## Mental model

**Say it in one breath:** tmux — window → full screen workspace

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

## Related

[[tmux]]
