[[Github action]] [[Github runner]] [[GIT/git command]]

# GitHub CLI (`gh`)

> Terminal client for GitHub — auth, PRs, issues, secrets, and API calls without clicking through the website.

## Interview Relevance

Interviewers look for PR workflow fluency (`create`/`checks`/`merge`), scripting with `--json`, and safe secret handling from the shell.

## Sources

- [GitHub CLI manual](https://cli.github.com/manual/) — deep-dive
- [GitHub Docs — GitHub CLI](https://docs.github.com/en/github-cli) — overview

## Key Concepts

- **Repo-aware defaults:** uses the current directory remote → fewer flags day to day.
- **Auth per host:** `github.com` or GHES via `--hostname`.
- **JSON + jq:** `--json` / `--jq` for scripts and incident tooling.
- **Secret scopes:** repository, environment, or org → match how Actions reads them.

## Technical Details

```bash
gh auth login
gh auth status
gh pr create --base main --title "fix: …" --body "…"
gh pr checks 42
gh pr merge 42 --squash --delete-branch
gh secret set API_KEY < secret.txt
gh api user --jq .login
```

| Symptom | Check | Fix |
|---------|-------|-----|
| HTTP 401 | `gh auth status` | `gh auth login` |
| Wrong repo | `gh repo view` | `cd` to root or `-R owner/repo` |
| Cannot set secret | Role | Need maintain/admin (or org role) |

## Real-World Applications

Incident response and local PR hygiene: open PR, watch checks, merge, without leaving the terminal.

**Example:** `gh pr checks` fails on fork secrets — expected; use trusted workflows or labels for deploy jobs.

## Pros/Cons or Trade-offs

- **Pro:** Fast, scriptable, consistent with browser features.
- **Con:** Still needs correct auth scopes; destructive commands exist (`repo delete`).

## Comparison

- vs browser UI: CLI wins for bulk/scripted ops; UI wins for visual review.
- vs raw REST: `gh api` is thinner than dedicated commands but more flexible.

## Mistakes to Avoid

- Echoing secrets into shell history — pipe from file/env.
- `gh repo delete --yes` without confirmation culture — prefer archive.
- Using long-lived PATs in dotfiles instead of `gh auth login` store.
