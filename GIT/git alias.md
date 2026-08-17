[[git command]] [[git branch]] [[git logs]] [[git formating]]

# Git aliases

> shortcuts for repeated flags — save typing, encode team conventions; prefer scripts (`!`) for shell pipelines.

```txt
        Git aliases ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers use `Git aliases` to check real Git fluency under pressure

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```
git st  →  alias.st = status -sb
git ignoredtop → !git ignored | cut ...
```

- **Note:** Aliases don't pass arguments the same way unless you use `$1` in shell aliases

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Typos in alias names** — `git ignoreedtop` vs `ignoredtop`; document team aliases in README.

> [!WARNING]
> **`git co` shadowing** — newcomers may not know real subcommand; document in onboarding.

> [!WARNING]
> **Shell injection in `!` aliases** — don't embed untrusted input.

| Symptom | Check | Fix |
|---------|-------|-----|
| Alias not found | Scope (global vs local) | `git config --list --show-origin \| grep alias` |
| `ignoredtop` typo fails | Wrong alias name | `git config --get alias.ignoredtop` |
| Shell alias no args | Missing `$@` | Use `!f() { ...; }; f'` pattern for args |
| Destructive alias | `!` with rm/reset | Code review aliases before sharing dotfiles |
| Works in bash not fish | Shell-specific | Use POSIX sh in `!` or external script |

## Pros/Cons or Trade-offs
- **Complex multi-step automation**
- **Override built-in commands**
