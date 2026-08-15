[[Bash]] [[Bash syntax]] [[bash script]] [[Scripting]]

# Bash history

> Bash history stores commands you ran — search, redo, and carefully avoid logging secrets.

## Interview Relevance
Interactive productivity (`!!`, Ctrl+R) plus ops hygiene: `HISTCONTROL`, `HISTIGNORE`, and not putting passwords on the command line.

## Sources
- [Bash Reference — Bash History Facilities](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html) — deep-dive
- [history(3) / bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html) — overview

## Core Definition
Commands may be saved to the in-memory history list and later to `~/.bash_history`. Interactive expansions (`!!`, `!$`) and Ctrl+R search the list. Options control size, duplicates, and ignored patterns.

## Key Concepts
- **HISTSIZE / HISTFILESIZE:** Memory vs on-disk retention.
- **HISTCONTROL:** `ignorespace`, `ignoredups`, `erasedups`.
- **HISTIGNORE:** Drop noisy commands (`ls`, `cd`).
- **history -a / -r:** Append/read without waiting for logout.
- **Secrets:** Leading space (with ignorespace) or avoid CLI secrets entirely.

## Technical Details

```bash
history
history -a
history -r
fc -l
fc -e nano 123

!!
!-2
!?install
!$
!^
^old^new^
!!:s/old/new/

export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth
export HISTIGNORE="ls:cd:pwd:history"
export HISTCONTROL=ignoredups:erasedups
```

| Symptom | Check | Fix |
|---------|-------|-----|
| History empty next login | HISTFILE / perms | Fix path; `history -a` |
| Secrets in file | pasting passwords | Rotate; HISTCONTROL; use prompts/files |
| Ctrl+R weak | no fzf | Install [[fzf]] bindings |
| Lost parallel-session cmds | default overwrite | `history -a` + `erasedups` patterns |

## Real-World Applications
Re-running a long deploy command with `!!`, editing a previous entry with `fc`, and configuring larger shared-safe history in `.bashrc`.

## Pros/Cons or Trade-offs
- **Pro:** Massive interactive speed-up.
- **Con:** Leak surface for secrets; multi-session merge quirks.
- **Trade-off:** Convenient expansions vs explicit scripts for anything important.

## Comparison
vs [[fzf]] Ctrl+R: better fuzzy search UI. vs script files: history is personal/ephemeral; scripts are reviewable. Related: [[Bash syntax]] history expansion.

## Mistakes to Avoid
- Putting tokens/passwords on the command line “just once.”
- Relying on `!!` inside scripts (history expansion is interactive-oriented).
- Assuming all parallel SSH sessions flush history cleanly by default.
