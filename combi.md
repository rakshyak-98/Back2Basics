[[Linux/commands/fzf]] [[Linux/CLI]]

# combi (rofi mode)

> Rofi **combi** mode merges window switcher, app launcher, and run dialog into one fuzzy search — muscle memory launcher on Linux desktops.

---

## How it works


Rofi is a dmenu replacement. **combi** aggregates multiple internal modes (`window`, `drun`, `run`) into a single filtered list. User types; rofi ranks matches across modes. Configured via CLI flags or `~/.config/rofi/config.rasi`.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **combi** | This note’s core idea | “I explain combi in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---


## Configuration and commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Broken / unexpected | Reproduce + logs | Fix config or code path |
| Works only locally | Env / secrets / versions | Align environments |
| Intermittent | race / timeout / retry | Add backoff; fix shared state |

---


## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---


## When not to use

- Skip when a simpler existing approach already fits.

---


## Related

[[Linux/commands/fzf]] [[Linux/CLI]]

## Sources

- [Wikipedia — combi](https://en.wikipedia.org/wiki/combi)
