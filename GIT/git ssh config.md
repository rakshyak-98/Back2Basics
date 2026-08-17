[[GIT]]

# git ssh config

> git ssh config — bad owner or permissions on /home/mihir/.ssh/config





## Interview Relevance
SSH config for Git checks host aliases, keys per host, and debugging permission denied.

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Technical Details
```bash
# ~/.ssh/config
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
chmod 600 ~/.ssh/config
```

## Pros/Cons or Trade-offs
- Do not disable `StrictHostKeyChecking` in production automation.

## Mistakes to Avoid
> [!WARNING]
> SSH config `Host` is a **label** — it does not have to match the real DNS name.

| Symptom | Check | Fix |
|---------|-------|-----|
| Bad owner or permissions on ~/.ssh/config | File mode or ownership | `chmod 600 ~/.ssh/config`; owned by your user |
| Wrong key offered | Multiple keys; no IdentitiesOnly | Set `IdentityFile` per Host block |
| Host key verification failed | DNS or MITM; rotated host key | Verify fingerprint; update `known_hosts` |
| Connection timed out | Firewall; wrong HostName | `ssh -vT git@github.com` |
