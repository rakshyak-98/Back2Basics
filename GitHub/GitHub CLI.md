[[GitHub CLI]] [[INDEX]]

# GitHub CLI

> GitHub CLI (gh) — auth, PRs, secrets, and API.

---

## GitHub CLI

From [[GitHub CLI]].

```bash
gh auth login
gh auth status
gh pr create --base main --title "fix: …" --body "…"
gh pr checks 42
gh pr merge 42 --squash --delete-branch
gh secret set API_KEY < secret.txt
gh api user --jq .login
```
