[[Github action]] [[Github runner]] [[GIT/git command]]

# GitHub CLI (`gh`)

> Terminal client for GitHub — auth, PRs, issues, secrets, and API calls without clicking through the website.

```txt
        GitHub CLI (`gh`) ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers look for PR workflow fluency (`create`/`checks`/`merge`), script…

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

## Mistakes to Avoid
- **Mistake:** Echoing secrets into shell history — pipe from file/env
- **Mistake:** `gh repo delete --yes` without confirmation culture
- **Mistake:** Using long-lived PATs in dotfiles instead of `gh auth login` sto…

## Pros/Cons or Trade-offs
- **Pro:** Fast, scriptable, consistent with browser features.
- **Con:** Still needs correct auth scopes; destructive commands exist (`repo delete`).

## Comparison
- vs browser UI: CLI wins for bulk/scripted ops; UI wins for visual review.
- vs raw REST: `gh api` is thinner than dedicated commands but more flexible.


### Use cases
- Incident response and local PR hygiene: open PR, watch checks, merge, without…

- **Example:** `gh pr checks` fails on fork secrets
