[[keyrings]] [[gpg]] [[keyctl]] [[commands/keyctl]] [[SSH]]

# Linux Key management

> Spans file-based secrets (PEM, gpg) and in-kernel keyrings (`keyctl`) — know which layer holds the credential.

## Interview Relevance

Security ops: 600 permissions, agents vs files, APT keyrings vs `keyctl`, and why agent forwarding extends trust.

## Sources

- `man 1 keyctl` — deep-dive
- [kernel key retention service](https://www.kernel.org/doc/html/latest/security/keys/core.html) — deep-dive

## Key Concepts

- **Disk secrets:** PEM/gpg files with strict modes.
- **Kernel keyrings:** RAM-backed keys via `keyctl`.
- **Agents:** `ssh-agent` / `gpg-agent` cache unlock.
- **APT keyrings:** repo metadata trust — [[keyrings]].

## Technical Details

```txt
disk:  *.pem / gpg homedir / keyrings/*.gpg
kernel: keyctl session/user keyrings
agents: ssh-agent, gpg-agent
```

```bash
sudo install -m 600 -o root -g root key.pem /etc/ssl/private/
keyctl show
keyctl add user mysecret pass:s3cr3t @u
gpg --list-secret-keys
ssh-add -l
```

| Knob | Why it matters |
|------|----------------|
| Mode bits | `644` secret files leak |
| Agent lifetime | Cached passphrases |

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied reading key | Owner/mode | `chown`/`chmod 600` |
| NO_PUBKEY apt | Keyring | Fix signed-by path |
| ssh asks passphrase always | Agent empty | `ssh-add`; check `SSH_AUTH_SOCK` |
| keyctl gone after logout | Session keyring | Link to user keyring / redesign persist |

## Real-World Applications

Install a TLS private key with `install -m 600`, keep SSH keys in an agent for deploys, and scope APT vendor keys under `/usr/share/keyrings`.

## Pros/Cons or Trade-offs

- **Pro:** Layered options from files to kernel to agents.
- **Con:** Easy to confuse layers; agents and forwarding create trust sprawl.

## Comparison

- vs Vault/KMS/SOPS: those scale fleet secrets; this note is host-local primitives.
- vs embedding keys in images: inject at runtime instead.

## Mistakes to Avoid

- Committing secrets then “fixing” with chmod — rotate.
- SSH agent forwarding to untrusted hosts.
- World-readable PEM under `/etc`.
