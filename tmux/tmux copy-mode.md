[[tmux]] [[Linux/CLI]]

# tmux copy-mode

> Keyboard selection from scrollback into tmux paste buffers — capture logs and commands without a mouse-only workflow.





## Interview Relevance
Ops interviews: navigate scrollback, copy text, paste across panes — especially on jump hosts without clipboard sharing.

## Sources
- [tmux — Buffers and copy mode](https://man.openbsd.org/tmux#WINDOWS_AND_PANES) — deep-dive

## Key Concepts
- **Copy-mode:** freeze pane view and move a cursor through history.
- **Paste buffer:** tmux-internal clipboard (can integrate with system clipboard via config).
- **Vi vs emacs keys:** mode-keys setting changes motions.

## Technical Details
```bash
# often: Ctrl-b [   enter copy-mode
# select, copy to buffer, Ctrl-b ] paste
tmux show-buffer
tmux list-buffers
```

With `mode-keys vi`, motions feel like vim visual mode inside the pane history.

| Task | Typical flow |
|------|----------------|
| Enter copy-mode | Prefix + `[` |
| Paste | Prefix + `]` |
| Search history | `/` or `?` in vi mode |

## Real-World Applications
Copy a failed migration error from scrollback into a ticket without re-running the command.

**Example:** SSH from a phone — mouse selection fails; copy-mode still works.

## Pros/Cons or Trade-offs
- **Pro:** Reliable remote copy when OS clipboard forwarding is broken.
- **Con:** Muscle memory differs per `mode-keys` and bindings.

## Comparison
- vs terminal emulator selection: emulator clipboard may not work over plain SSH; tmux buffers do.
- vs [[tmux]] basics: copy-mode is scrollback UX inside the multiplexer.

## Mistakes to Avoid
- Confusing tmux buffer with the OS clipboard (needs explicit integration).
- Exiting copy-mode before copying.
- Huge scrollback eating memory — set history limits thoughtfully.
