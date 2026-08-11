[[apache]]

# apache command

> apache command — enables the Apache module named mod_rewrite.

---

## Mental model

**Say it in one breath:** apache command — plain job, how I run it, how I know it’s broken.


```bash
sudo a2enmod rewrite;
```
- enables the Apache module named `mod_rewrite`.
- `mod_rewrite` is a built-in Apache module that allows rewriting requested URLs on the fly.
- it commonly used to convert clean URLs like `/blog/post-title` into actual internal file paths like `index.php?post=post-title`.
- it was likely disabled by default on your system, which is common for Apache installs.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **apache command** | Core idea of this note | “I can explain apache command without jargon.” |
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

[[apache]]
