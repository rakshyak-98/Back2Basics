[[Python]]

# Python

> Python — 3 -m pdb <"python file to debug">;

---

## Mental model

**Say it in one breath:** Python — 3 -m pdb <"python file to debug">;

- reference
	[https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/)
	[https://docs.python.org/3/library/inspect.html#module-inspect](https://docs.python.org/3/library/inspect.html#module-inspect)
	[https://docs.python.org/3/glossary.html](https://docs.python.org/3/glossary.html)
	[https://web.stanford.edu/class/physics91si/2013/handouts/Pdb_Commands.pdf](https://web.stanford.edu/class/physics91si/2013/handouts/Pdb_Commands.pdf)
```bash
python3 -m pdb <"python file to debug">;
```
- dashes are illegal in Python identifiers
- The `sys.path` list contains all the directories that Python will search for modules when you try to import them.


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Python]]
