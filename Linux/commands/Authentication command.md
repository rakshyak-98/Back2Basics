[[commands]] [[SSH]] [[gpg]] [[keyrings]]

# Authentication command

> Host and user crypto helpers — ssh-keygen/keyscan/ssh-add for SSH trust; gpg for signing and encrypting.

## Mental model

**Say it in one breath:** SSH proves *server* identity via `known_hosts` and *user* via keypairs; GPG proves *you* signed or encrypted data.

```txt
SSH:  client ──► verify host key (known_hosts)
              ──► prove user (private key / agent)

GPG:  sign / encrypt with your keyring; verify with their public key
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`known_hosts`** | Cached server public keys | “Stops MITM if the host key suddenly changes.” |
| --- | --- | --- |
| **`ssh-keyscan`** | Fetch host key without login | “Pre-seed CI known_hosts carefully.” |
| **`ssh-copy-id`** | Install your pubkey | “Drops into `authorized_keys`.” |
| **`ssh-add`** | Load key into agent | “Unlock once; use many times.” |
| **GPG sign** | Detached / clear signature | “Git `-S` uses your signing key.” |

## SSH trust & keys

```bash
# Host keys
ssh-keyscan hostname
ssh-keyscan -p 2222 hostname
ssh-keyscan hostname >> ~/.ssh/known_hosts
ssh-keygen -R hostname              # remove stale host key

# User keys / agent
ssh-keygen -t ed25519 -C "you@example"
ssh-copy-id user@remote-host
ssh-add -l
ssh -v user@hostname                # auth debug

# known_hosts line shape
# hostname algorithm public-key
```

On first connect, SSH prompts and stores the host key; later mismatches = warning (possible MITM or legitimate reinstall).

## GPG for commits / files

```bash
sudo apt install gnupg
gpg --full-gen-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <keyid>
gpg --armor --export-secret-keys <keyid>   # protect this

git config --global user.signingkey <keyid>
git config --global commit.gpgsign true
git commit -S -m "signed"
git log --show-signature
```

Deeper encrypt/sign operations: [[gpg]].

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | Reimage vs attack | Verify out-of-band; then `ssh-keygen -R host` |
| Permission denied (publickey) | Wrong key / agent | `ssh -v`; `ssh-add -l`; correct `IdentityFile` |
| `ssh-copy-id` fails | Password auth disabled | Install pubkey via console/cloud-init |
| Git says no secret key | Wrong `signingkey` | `gpg --list-secret-keys`; fix git config |
| Agent empty after reboot | No auto-start | `ssh-add` / keychain / systemd user unit |

## Gotchas

> [!WARNING]
> **Blind `ssh-keyscan >> known_hosts` in CI** — you trust whatever answers on the network that day. Pin fingerprints when you can.

> [!WARNING]
> **Host key change can be legitimate** — still verify via cloud console fingerprint before removing the old entry.

> [!WARNING]
> **Exporting secret GPG keys** — treat `.asc` like a password dump.

## When NOT to use

- **application-level OAuth/OIDC** — different layer than SSH host trust.
- **TLS cert management** — certbot/ACME, not ssh-keyscan.
- **Full GPG keyring operations** — see dedicated [[gpg]] note.

## Related

[[SSH]] [[gpg]] [[keyrings]] [[visudo]] [[commands]]
