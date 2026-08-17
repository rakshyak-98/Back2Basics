[[GIT]]

# 1. When git runs a command like `git push` it internally calls.

> 1. When git runs a command like `git push` it internally calls. — create auth token from GitHub personal access token

```txt
        1. When git runs a ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers use `1

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
### reset the credential manager
```bash
- **Note:** git config --global --unset credentila.*; # remove the set credential helper
git clone <https remote repo url>;
git pull; # git will ask the username and auth token.
```
- **create authentication:** create authentication token from [GitHub personal access token](https://githu…
- **paste the:** paste the authentication token password.
```bash
git config --global credential.helper cache;
```
- **the `cache`:** the `cache` helper stores credentials in memory only, not on disk.
- **Git spawn:** Git spawn the credentials cache daemon in the background.
- **it keeps:** it keeps the credentials in RAM for 15 minutes by default.
- **no file:** no file is written.
- **once expired:** once expired or system restarts -> the data is gone.
```bash
- **Note:** printf "protocol=https\nhost=github.com\n\n" | git credential fill;
```

## Technical Details
```bash
git config --global credential.helper cache
git config --global --unset credential.helper
git credential reject   # paste host=... protocol=https
```

## Mistakes to Avoid
> [!WARNING]
> Git credential helpers store secrets on disk or in the OS keychain — lock your workstation.

| Symptom | Check | Fix |
|---------|-------|-----|
| Repeated password prompts | Helper not configured | Set `credential.helper` or use SSH remote |
| Stored wrong password | Cached credentials | `git credential reject`; clear OS keychain entry |
| Token works in browser not git | Using account password not PAT | Create personal access token; use as password |
| HTTPS 401 after password change | Stale cache | Unset helper cache; re-authenticate |

## Pros/Cons or Trade-offs
- Do not embed tokens in remote URLs committed to the repository.
