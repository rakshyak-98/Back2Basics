[[vim buffers]] [[Descriptive/LSP]] [[nvim setup]] [[zed keybindings]]

# Vim / Neovim keybindings — go to

> LSP-powered navigation (definition, references, implementation) plus jump-back — requires Neovim with a language server attached; plain Vim needs ctags or a plugin.

---

## Index

- [[#Quick reference]]
- [[#Standard config / commands]]
- [[#Options / flags]]
- [[#Mental model]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Examples]]
- [[#Related]]

## Quick reference

| Task | Command |
|------|---------|
| … | `…` |

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Options / flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

## Mental model

**Say it in one breath:** Vim / Neovim keybindings — go to — I can explain the job, the configuration, and the top failure without jargon.


**Go to** commands ask the [[Descriptive/LSP|LSP]] (or ctags) where a symbol lives, then jump the cursor there. Neovim 0.11+ ships **global** `gr*` maps at startup; **buffer-local** maps (`K`, `CTRL-]`, diagnostics) apply when an LSP client attaches.

After any jump, use the **jumplist** (`Ctrl-o` / `Ctrl-i`) or **tag stack** (`Ctrl-t`) to return — LSP single-result jumps push onto the tag stack.

```
cursor on symbol → go-to key → LSP query → jump (or quickfix list)
                                    ↓
                              Ctrl-o to jump back
```

See [[Descriptive/LSP#Difference between Go to Reference, Definition, Implementation]] for when to use each target.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Vim / Neovim keybindings — go to** | This note’s core idea | “I explain Vim / Neovim keybindings — go to in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Triage (when things break)

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

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Examples

```bash
# …
```

## Related

[[vim buffers]] [[Descriptive/LSP]] [[nvim setup]] [[zed keybindings]]
