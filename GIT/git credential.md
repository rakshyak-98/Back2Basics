[[GIT]]

# 1. When git runs a command like `git push` it internally calls.

> 1. When git runs a command like `git push` it internally calls. — create auth token from GitHub personal access token





## Interview Relevance
Interviewers use `1. When git runs a command like `git push` it internally calls.` to check real Git fluency under pressure — history rewriting safety, conflict recovery, and what not to do on shared branches.

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
### reset the credential manager
```bash
git config --global --unset credentila.*; # remove the set credential helper
git clone <https remote repo url>;
git pull; # git will ask the username and auth token.
```
- create authentication token from [GitHub personal access token](https://github.com/settings/tokens)
- paste the authentication token password.
```bash
git config --global credential.helper cache;
```
- the `cache` helper stores credentials in memory only, not on disk.
- Git spawn the credentials cache daemon in the background.
- it keeps the credentials in RAM for 15 minutes by default.
- no file is written.
- once expired or system restarts -> the data is gone.
```bash
printf "protocol=https\nhost=github.com\n\n" | git credential fill;
```

## Technical Details
```bash
git config --global credential.helper cache
git config --global --unset credential.helper
git credential reject   # paste host=... protocol=https
```

## Pros/Cons or Trade-offs
- Do not embed tokens in remote URLs committed to the repository.

## Mistakes to Avoid
> [!WARNING]
> Git credential helpers store secrets on disk or in the OS keychain — lock your workstation.

| Symptom | Check | Fix |
|---------|-------|-----|
| Repeated password prompts | Helper not configured | Set `credential.helper` or use SSH remote |
| Stored wrong password | Cached credentials | `git credential reject`; clear OS keychain entry |
| Token works in browser not git | Using account password not PAT | Create personal access token; use as password |
| HTTPS 401 after password change | Stale cache | Unset helper cache; re-authenticate |
