[[GIT]] [[DevOps/Jenkins]] [[Deployment/spinnaker]]

# GitHub CLI (`gh`)

> Terminal interface for auth, PRs, issues, secrets, and API — faster than clicking through github.com during incidents.

## Mental model

`gh` wraps GitHub REST/GraphQL with repo-aware defaults (current directory's remote). Auth is per-host (`github.com`, GHES). Most commands accept `--json` for scripting. Secrets and variables are scoped: repo, environment, or org.

## Standard config / commands

### Auth (once per machine)

```bash
gh auth login                    # browser or token
gh auth status
gh auth switch --hostname github.com --user other-account
gh api user --jq '.login'
```

### PR workflow

```bash
gh pr create --base main --head feature/x --title "fix: …" --body "…"
gh pr view 42 --web
gh pr checks 42
gh pr merge 42 --squash --delete-branch
gh pr diff 42
```

### Issues & labels

```bash
gh label create bug --description "Something broken" --color d73a4a
gh issue create --title "…" --body "…" --label bug
gh issue edit 12 --add-label bug
```

### Secrets (CI)

```bash
gh secret set API_KEY --body "$API_KEY"
gh secret set API_KEY --env production --body "$API_KEY"
gh secret list --env production
```

### Repo ops

```bash
gh repo view --json sshUrl,defaultBranchRef
gh repo clone owner/repo
gh repo delete owner/repo --yes   # destructive; needs admin
```

### Scripting

```bash
gh pr list --json number,title,author --jq '.[] | "\(.number) \(.title)"'
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `HTTP 401` | `gh auth status` | `gh auth login` or refresh token |
| `HTTP 403` on secret set | Repo admin? | Need maintain/admin; org secrets need org role |
| Wrong repo context | `gh repo view` | `cd` to repo root or `-R owner/repo` |
| `gh pr create` no commits | `git status` | Push branch first |
| API rate limit | `gh api rate_limit` | Wait or use PAT with higher limit |

## Gotchas

> [!WARNING]
> **`gh repo delete --yes`** — no undo; prefer archive for mistakes.
>
> **Secrets echo in shell history** — pipe from file or env: `gh secret set KEY < secret.txt`.
>
> **GHES hostname** — must pass `--hostname` on every command or set default during login.

## When NOT to use

- Don't use `gh` in CI instead of `GITHUB_TOKEN` + native actions — use `gh` locally and in ad-hoc scripts.
- Don't store long-lived PATs in shell profiles — use `gh auth login` credential store.

## Related

[[Github runner]] [[Github action]] [[GIT/git command]] [[gpg sign]]
