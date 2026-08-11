[[zed config]] [[Descriptive/vscode]]

# Zed keybindings

> Zed keybindings — when the LSP popup and a ghost prediction conflict, hold alt to preview inline and hide the menu. See [[zed config#Inline ghost…

---

## Mental model

**Say it in one breath:** Zed keybindings — plain job, how I run it, how I know it’s broken.


### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Zed keybindings** | Core idea of this note | “I can explain Zed keybindings without jargon.” |
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

[[zed config]]] [[[Descriptive/vscode]]
