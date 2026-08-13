[[GIT]]

# 1. When git runs a command like `git push` it internally calls.

> 1. When git runs a command like `git push` it internally calls. — create auth token from GitHub personal access token

---

## How it works

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


## Configuration and commands

```bash
git config --global credential.helper cache
git config --global --unset credential.helper
git credential reject   # paste host=... protocol=https
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Repeated password prompts | Helper not configured | Set `credential.helper` or use SSH remote |
| Stored wrong password | Cached credentials | `git credential reject`; clear OS keychain entry |
| Token works in browser not git | Using account password not PAT | Create personal access token; use as password |
| HTTPS 401 after password change | Stale cache | Unset helper cache; re-authenticate |

---


## Gotchas

> [!WARNING]
> Git credential helpers store secrets on disk or in the OS keychain — lock your workstation.

---


## When not to use

- Do not embed tokens in remote URLs committed to the repository.


---


## Related

[[GIT]]

## Sources

- [Wikipedia — git credential](https://en.wikipedia.org/wiki/git_credential)
