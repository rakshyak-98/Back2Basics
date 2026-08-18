[[Bash]] [[bash script]] [[bash flags]] [[Bash history]]

# Bash syntax

> Bash syntax is how the shell parses words, expansions, and control operators — so pipelines and scripts do what you meant.

## Mental model

**Say it in one breath:** the shell splits into words, expands (`$`, globs, `!!`), then runs — operators like `&&` / `|` connect commands, not strings.

```txt
line ──► tokenize ──► expand ──► redirections ──► execute
         "…" / '…'     $VAR `…`  > >> <   && || | ; ( )
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`&&` / `\|\|`** | Conditional chain | “Next runs only if previous succeeded / failed.” |
| --- | --- | --- | --- | --- |
| **`$(…)` / `` `…` ``** | Command substitution | “Prefer `$()` — nests cleanly.” |
| **`[[ … ]]`** | Bash test | “Safer than `[` for strings and patterns.” |
| **`--`** | End of options | “Protects filenames starting with `-`.” |
| **Subshell `(…)`** | Nested environment | “`cd` inside doesn’t move the parent shell.” |
| **`${var:-default}`** | Default if unset | “Parameter expansion beats sprawling ifs.” |

## Standard config / commands

```bash
# Chains / grouping
mkdir -p new_dir && cd new_dir
cmd1 || echo "failed"
(cd /tmp && ls)                 # cwd restored after

# End of options
touch -- -file.txt
rm -- -file.txt

# Process substitution
diff <(ls dir1) <(ls dir2)

# Parameter expansion
echo "${my_var:-default}"
echo "${my_var:0:3}"

# History expansion (interactive)
!!
!-2

# Safe script header trio — see [[bash flags]]
set -euo pipefail
```

| Construct | Job |
| --- | --- |
| `"$var"` | Expand but keep as one word |
| `'$var'` | Literal |
| `${#arr[@]}` | Array length |
| `$(( … ))` | Integer arithmetic |

`fc` helpers: `fc -ln -1` (last command), `fc -e nano` (edit prior).

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Word-splitting bugs | Unquoted `$var` | Always quote: `"$var"` |
| Glob ate my args | Unquoted `*` | Quotes or `set -f` temporarily |
| `-file` parsed as flag | Leading dash | Insert `--` |
| `cd` “stuck” in scripts | Subshell vs source | `(cd …)` vs plain `cd` deliberately |
| `[[ = ]]` surprises | Pattern vs string | Use `==` carefully; quote the right side if literal |

## Gotchas

> [!WARNING]
> **`[ $var = x ]` breaks on empty/spaces** — use `[[ "$var" == x ]]` or quote inside `[`.

> [!WARNING]
> **`$*` vs `$@`** — `"$@"` preserves argument boundaries; `"$*"` joins.

> [!WARNING]
> **History expansion in scripts** is usually off — `!!` is an interactive habit.

## When NOT to use

- **Heavy data munging** — Python; keep bash as the glue.
- **POSIX-strict `/bin/sh` scripts** — avoid Bashisms (`[[`, arrays) or set `#!/bin/bash`.
- **Complex JSON** — [[jq]].

## Related

[[bash script]] [[bash flags]] [[Bash history]] [[tee]] [[Bash]]
