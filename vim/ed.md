[[vim]]

# ed

> ed — 1 # go to first line

---

## Mental model

**Say it in one breath:** ed — plain job, how I run it, how I know it’s broken.


| Command      | Description           |
| ------------ | --------------------- |
| `e filename` | Open file for editing |
| `w`          | Write changes to file |
| `w filename` | Write to new file     |
| `q`          | Quit                  |
| `q!`         | Quit without saving   |
| Command | Description                  |
| ------- | ---------------------------- |
| `1`     | Go to first line             |
| `$`     | Go to last line              |
| `.`     | Current line                 |
| `n`     | Show line number and content |
| Command | Description                            |
| ------- | -------------------------------------- |
| `a`     | Append after current line (`.` to end) |
| `i`     | Insert before current line             |
| `c`     | Change current line                    |
| `.`     | End input mode                         |
| Command | Description         |
| ------- | ------------------- |

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ed** | Core idea of this note | “I can explain ed without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

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

[[vim]]
