[[GIT]]

# git repo config

> git repo config — know what it does, how to configure it, and how it fails in production.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** git repo config is infra/security tooling — least privilege, clear config, observable failures.


```shell
gpg --full-generate-key; # generate gpg key
gpg --list-secret-keys --keyid-format=long;
gpg --armor --export <your email>; # export your public key
```
```shell
git config --get commit.gpgsign;
git log --show-signature;
```
#### Configure git to use GPG key
```shell
git config user.signingkey <gpg key>;
git config commit.gpgsign true; # enable auto-sign
git config tag.gpgsign; # enable auto sign for tags
```
```shell
git commit -S -m <commit message>; # if auto-sign is not eanble
```
#### SSH
```shell
git conifg gpg.format ssh;
git config user.signingkey <path to ssh .pub file>;
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **git repo config** | Core idea of this note | “I can explain git repo config without jargon.” |
| **least privilege** | Only needed access | “Grant the smallest role that works.” |
| **secret** | Password/key/token | “Secrets out of git; rotate them.” |
| **observability** | metrics/logs/traces | “You can’t fix what you can’t see.” |

---

## Standard config / commands

```bash
# status
# check version, auth, and recent changes
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail | clock / creds / IAM | Sync time; fix policy |
| TLS error | cert chain / SNI | Fix certs and CA bundle |
| Deploy down | rollback / health | Roll back; check probes |

---

## Gotchas

> [!WARNING]
> Never commit long-lived secrets.

---

## When NOT to use

- Don’t build custom infra when managed services meet the SLO.

---

## Related

[[GIT]]
