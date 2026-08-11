[[Bash]] [[Bash syntax]] [[bash script]]

# Bash history

> Bash history stores commands you ran — search, redo, and (carefully) avoid logging secrets.

---

## Mental model

**Say it in one breath:** session list in memory, file usually `~/.bash_history`; expansions like `!!` replay; `HISTCONTROL`/`HISTIGNORE` filter what gets saved.

```txt
typed command ──► maybe save (HISTIGNORE / ignorespace)
                     ↓
              history list ──► ~/.bash_history (on exit / history -a)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`!!` / `!-2`** | Last / Nth prior | “Redo without retyping.” |
| **`!$` / `!^`** | Last / first arg of prior | “Reuse paths quickly.” |
| **`HISTCONTROL=ignoreboth`** | Skip dups + leading-space | “Space-prefix keeps secrets out of history.” |
| **`HISTIGNORE`** | Pattern denylist | “Don’t save `ls`/`cd` noise.” |
| **`history -a` / `-r`** | Append / read file | “Share history across sessions deliberately.” |

---

## Standard config / commands

```bash
history
history -a                          # append live session → file
history -r                          # read file into session
fc -l
fc -e nano 123                      # edit entry 123

# Expansions (interactive)
!!
!-2
!?install
!$                                  # last arg of previous
!^                                  # first arg
^old^new^                           # quick substitute
!!:s/old/new/

# ~/.bashrc knobs
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth       # ignorespace + ignoredups
export HISTIGNORE="ls:cd:pwd:history"
export HISTCONTROL=ignoredups:erasedups
```

Leading space before a command → often omitted from history when `ignorespace`/`ignoreboth` is set — useful for ` export API_KEY=…`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| History empty in new shell | HISTFILE / permissions | `echo "$HISTFILE"`; fix mode |
| Secrets in history | Pasted passwords | `history -d N`; rotate secret; enable ignoreboth |
| Missing commands from other tmux panes | No share config | `history -a` / `PROMPT_COMMAND` append patterns |
| `!!` literal in script | History off in non-interactive | Don’t rely on it in scripts |
| Duplicates forever | No erasedups | Set `ignoredups:erasedups` |

---

## Gotchas

> [!WARNING]
> **History is plaintext** — never assume `~/.bash_history` is safe; lock down home perms.

> [!WARNING]
> **`history -c` clears memory, not always the file** — truncate `HISTFILE` if you mean it.

> [!WARNING]
> **Shared NFS homes** — concurrent writers can clobber history; accept loss or use careful append strategies.

---

## When NOT to use

- **Audit of who ran what on a server** — central auditd/SIEM, not per-user bash history.
- **Structured runbooks** — real scripts in git ([[bash script]]).
- **Password managers** — don’t paste secrets into the shell if you can avoid it.

---

## Related

[[Bash syntax]] [[bash script]] [[bash flags]] [[Bash]]
