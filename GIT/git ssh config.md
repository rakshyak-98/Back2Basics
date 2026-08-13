<!-- note-strategy: operational -->
[[GIT]]

# git ssh config

> git ssh config — bad owner or permissions on /home/mihir/.ssh/config

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** git ssh configuration — bad owner or permissions on /home/mihir/.ssh/config

## Standard config / commands

```bash
# ~/.ssh/config
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
chmod 600 ~/.ssh/config
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Bad owner or permissions on ~/.ssh/config | File mode or ownership | `chmod 600 ~/.ssh/config`; owned by your user |
| Wrong key offered | Multiple keys; no IdentitiesOnly | Set `IdentityFile` per Host block |
| Host key verification failed | DNS or MITM; rotated host key | Verify fingerprint; update `known_hosts` |
| Connection timed out | Firewall; wrong HostName | `ssh -vT git@github.com` |

---

## Gotchas

> [!WARNING]
> SSH config `Host` is a **label** — it does not have to match the real DNS name.

---

## When NOT to use

- Do not disable `StrictHostKeyChecking` in production automation.


---

## Related

[[GIT]]
