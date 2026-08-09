[[management]] [[keyrings]] [[gpg]] [[keyctl]]

# Linux Key management

> Linux key management spans file-based secrets (gpg, PEM) and in-kernel keyrings (`keyctl`) — know which layer holds the credential.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** long-lived trust in files/HSM; short-lived session creds in kernel keyrings; agents (ssh-agent/gpg-agent) broker use.

```txt
disk:  *.pem / gpg homedir / keyrings/*.gpg
kernel: keyctl session/user keyrings
agents: ssh-agent, gpg-agent
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **keyring (APT)** | Repo trust keys | “Verify apt metadata.” |
| **keyctl** | Kernel keys CLI | “RAM-backed secrets possible.” |
| **gpg-agent** | Private key broker | “Pins passphrase cache.” |
| **ssh-agent** | SSH key broker | “Forward carefully.” |
| **permissions** | 600 / root | “Secret files must not be world-readable.” |

---

## Standard config / commands

```bash
# file perms
sudo install -m 600 -o root -g root key.pem /etc/ssl/private/
# kernel
keyctl show
keyctl add user mysecret pass:s3cr3t @u
# gpg
gpg --list-secret-keys
# ssh
ssh-add -l
```

| Knob | Why it matters |
|------|----------------|
| Mode bits | Leak via `644` is common |
| Agent lifetime | Cached passphrases |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied reading key | Owner/mode | `chown`/`chmod 600` |
| NO_PUBKEY apt | Keyring | Fix signed-by keyring |
| ssh asks passphrase always | Agent empty | `ssh-add`; check `SSH_AUTH_SOCK` |
| keyctl gone after logout | Session keyring | Link to user keyring / persist design |

---

## Gotchas

> [!WARNING]
> **Secrets in world-readable git** — rotate immediately; chmod can’t un-leak.

> [!WARNING]
> **SSH agent forwarding** extends trust to the remote host.

---

## When NOT to use

- **App secrets at scale** — use a secrets manager (Vault/SOPS/cloud KMS).
- **Embedding keys in images** — inject at runtime.

---

## Related

[[keyrings]] [[keyctl]] [[gpg]] [[SSH]]
