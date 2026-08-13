[[git command]] [[git branch]] [[git logs]]

# Git aliases

> shortcuts for repeated flags — save typing, encode team conventions; prefer scripts (`!`) for shell pipelines.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Git aliases live in configuration (`~/.gitconfig` or repository `.git/config`). Simple aliases expand to subcommands; **`!` prefix** runs shell — full power, full footgun.


```
git st  →  alias.st = status -sb
git ignoredtop → !git ignored | cut ...
```

Aliases don't pass arguments the same way unless you use `$1` in shell aliases — for parameterized workflows use scripts in `PATH` or functions.

## Standard config / commands

### Simple aliases

```bash
git config --global alias.st 'status -sb'
git config --global alias.co 'checkout'
git config --global alias.br 'branch -vv'
git config --global alias.lg "log --graph --oneline --decorate -20"
```

### Shell pipeline alias

```bash
git config --global alias.ignored 'ls-files --ignored --exclude-standard --others'

git config --global alias.ignoredtop '!git ignored | cut -d "/" -f1 | sort -u'
```

Usage:

```bash
git ignoredtop
```

### List / remove

```bash
git config --global --get-regexp alias
git config --global --unset alias.st
```

### Repo-local alias (team convention)

```bash
git config alias.review 'log --oneline main..HEAD'
```

### Safe patterns

```bash
# visual diff tool
git config --global alias.difft 'difftool -d vimdiff'

# prune merged branches (interactive caution)
git config --global alias.cleanup '!git branch --merged main | grep -v "main" | xargs -r git branch -d'
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Alias not found | Scope (global vs local) | `git config --list --show-origin \| grep alias` |
| `ignoredtop` typo fails | Wrong alias name | `git config --get alias.ignoredtop` |
| Shell alias no args | Missing `$@` | Use `!f() { ...; }; f'` pattern for args |
| Destructive alias | `!` with rm/reset | Code review aliases before sharing dotfiles |
| Works in bash not fish | Shell-specific | Use POSIX sh in `!` or external script |

## Gotchas

> [!WARNING]
> **Typos in alias names** — `git ignoreedtop` vs `ignoredtop`; document team aliases in README.

> [!WARNING]
> **`git co` shadowing** — newcomers may not know real subcommand; document in onboarding.

> [!WARNING]
> **Shell injection in `!` aliases** — don't embed untrusted input.

## When NOT to use

- **Complex multi-step automation** — shell script in repository `scripts/` with tests.
- **Override built-in commands** — avoid aliasing `commit`/`push` to dangerous defaults.

## Related

[[git command]] [[git logs]] [[git formating]] [[git branch]]
