[[Bash]] [[Bash syntax]] [[bash script]] [[Scripting]]

# Bash history

> Bash history stores commands you ran — search, redo, and carefully avoid logging secrets.

```txt
        Bash history ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Interactive productivity (`!!`, Ctrl+R) plus ops hygiene: `HISTCONTROL`, `HIS…

## Sources
- [Bash Reference — Bash History Facilities](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html) — deep-dive
- [history(3) / bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html) — overview

## Key Concepts
- **HISTSIZE / HISTFILESIZE:** Memory vs on-disk retention.
- **HISTCONTROL:** `ignorespace`, `ignoredups`, `erasedups`.
- **HISTIGNORE:** Drop noisy commands (`ls`, `cd`).
- **history -a / -r:** Append/read without waiting for logout.
- **Secrets:** Leading space (with ignorespace) or avoid CLI secrets entirely.


- **Core:** Commands may be saved to the in-memory history list and later to `~/.bash_his…

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

## Mistakes to Avoid
- **Mistake:** Putting tokens/passwords on the command line “just once.”
- **Mistake:** Relying on `!!` inside scripts (history expansion is interactive…
- **Mistake:** Assuming all parallel SSH sessions flush history cleanly by defa…

## Pros/Cons or Trade-offs
- **Pro:** Massive interactive speed-up.
- **Con:** Leak surface for secrets; multi-session merge quirks.
- **Trade-off:** Convenient expansions vs explicit scripts for anything important.

## Comparison
- vs [[fzf]] Ctrl+R: better fuzzy search UI. vs script files: history is person…


### Use cases
- Re-running a long deploy command with `!!`, editing a previous entry with `fc…
