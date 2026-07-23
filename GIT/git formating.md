[[git logs]] [[git command]] [[git alias]]

# Git log formatting

> One-line: `--pretty=format` placeholders and presets — readable history for terminals, CI artifacts, and release notes (filename uses legacy typo *formating*).

## Mental model

`git log` output is templated. **`--pretty=format:"..."`** uses placeholders; **`--oneline`** and **`--medium`** are presets. Combine with `--graph`, `--decorate`, `--date=iso` for dashboards.

```
git log --pretty=format:"%h %ad | %an | %s" --date=short
         └─ hash  date      author  subject
```

**Author** (`%an`) wrote the patch; **committer** (`%cn`) applied it — differ after rebase/cherry-pick.

## Standard config / commands

### Common one-liners

```bash
git log --pretty=format:"%h - %an (%ar): %s"
git log --pretty=format:"%h %ad %s" --date=short
git log --graph --oneline --decorate --all
git log --pretty=fuller -3
```

### Placeholder reference

| Placeholder | Description |
|-------------|-------------|
| `%h` | Abbreviated commit hash |
| `%H` | Full commit hash |
| `%s` | Subject (first line of message) |
| `%b` | Body |
| `%an` | Author name |
| `%ae` | Author email |
| `%ad` | Author date |
| `%ar` | Author date, relative |
| `%cn` | Committer name |
| `%ce` | Committer email |
| `%cd` | Committer date |
| `%cr` | Committer date, relative |
| `%d` | Ref names (branches, tags) |
| `%D` | Ref names without wrapping parens |
| `%P` | Parent hashes |
| `%T` | Tree hash |

### Date formats

```bash
git log --date=iso --pretty=format:"%h %ad %s"
git log --date=format:'%Y-%m-%d %H:%M' --pretty=format:"%ad %s"
```

### Machine-readable (release notes script)

```bash
git log main..HEAD --pretty=format:"- %s (%h)" --no-merges
git log --pretty=format:'{%n  "hash": "%H",%n  "author": "%an",%n  "subject": "%s"%n},'
```

### Alias (see [[git alias]])

```bash
git config --global alias.lol "log --graph --pretty=format:'%Cred%h%Creset - %C(yellow)%ad%Creset %s %Cgreen(%an)%Creset' --date=short -20"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Literal `%h` in output | Missing `--pretty=format` | Quote format string |
| Wrong timezone on `%ad` | `--date` default | `--date=local` or `--date=iso-strict` |
| Empty `%d` | Detached or no refs | Normal for old commits |
| Garbled colors in CI | `%Cred` color codes | Drop `%C…` for plain logs |
| `%s` multiline breaks parser | Subject has newline | Use `%s` with `--no-merges` filter |

## Gotchas

> [!WARNING]
> **Rebase changes committer date** — `%cr` may say "2 minutes ago" for old work.

> [!WARNING]
> **Email in logs** — PII in shared CI logs; redact `%ae` for public artifacts.

> [!WARNING]
> **Shell quoting** — nested quotes in aliases break zsh/bash differently; test both.

## When NOT to use

- **Structured JSON export at scale** — `git cat-file`, libgit2, or platform API.
- **File content history** — add `-p` or use [[git diff]].

## Related

[[git logs]] [[git alias]] [[git command]] [[Release cycle]]
