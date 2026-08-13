[[vim]]

# ed

> ed — 1 # go to first line

---

## How it works

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


---


## Configuration and commands

```bash
# version + config path
# dry-run when available
```

---


## When things break

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


## When not to use

- Avoid the tool if a simpler built-in covers the job.

---


## Related

[[vim]]

## Sources

- [Wikipedia — ed](https://en.wikipedia.org/wiki/ed)
