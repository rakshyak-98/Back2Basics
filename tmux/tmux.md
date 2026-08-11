[[tmux]]

# tmux

> tmux — window → full screen workspace

---

## Mental model

**Say it in one breath:** tmux — plain job, how I run it, how I know it’s broken.


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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **tmux** | Core idea of this note | “I can explain tmux without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[tmux]]
