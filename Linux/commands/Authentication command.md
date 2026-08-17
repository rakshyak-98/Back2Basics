[[SSH]] [[gpg]] [[keyrings]] [[visudo]] [[Commands]] [[ssh agent]]

# Authentication command

> Host and user crypto helpers — ssh-keygen/keyscan/ssh-add for SSH trust; gpg for signing and encrypting.

```txt
        Authentication com ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Separates host-key trust from user auth, and shows safe CI known_hosts practi…

## Sources
- [ssh-keygen(1)](https://man.openbsd.org/ssh-keygen) — deep-dive
- [GnuPG manual](https://www.gnupg.org/documentation/) — overview

## Key Concepts
- **known_hosts:** Cached server public keys — mismatch warning.
- **ssh-keyscan:** Fetch host key without login — pin fingerprints when possible.
- **ssh-copy-id / ssh-add:** Install pubkey; load key into agent.
- **GPG signing:** Detached/clear signatures; Git `user.signingkey`.
- **Layering:** SSH/GPG ≠ OAuth/OIDC or TLS/ACME.


- **Core:** SSH trust has two layers: verify the **server** (`known_hosts`) then prove th…

## Technical Details
```bash
ssh-keyscan hostname
ssh-keyscan -p 2222 hostname
ssh-keygen -R hostname

ssh-keygen -t ed25519 -C "you@example"
ssh-copy-id user@remote-host
ssh-add -l
ssh -v user@hostname

sudo apt install gnupg
gpg --full-gen-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <keyid>

git config --global user.signingkey <keyid>
git config --global commit.gpgsign true
git commit -S -m "signed"
git log --show-signature
```

| Symptom | Check | Fix |
|---------|-------|-----|
| HOST IDENTIFICATION CHANGED | Reimage vs attack | Verify OOB; then `ssh-keygen -R` |
| Permission denied (publickey) | Wrong key/agent | `ssh -v`; `ssh-add -l`; `IdentityFile` |
| ssh-copy-id fails | Password auth off | Install pubkey via console/cloud-init |
| Git no secret key | Wrong signingkey | `gpg --list-secret-keys`; fix git config |
| Agent empty after reboot | No auto-start | `ssh-add` / keychain / user unit |

## Mistakes to Avoid
- **Mistake:** Blind `ssh-keyscan >> known_hosts` in CI without verification
- **Mistake:** Exporting secret GPG keys into chat/tickets
- **Mistake:** Treating a host key change as “always safe to accept.”

## Pros/Cons or Trade-offs
- **Pro:** Standard ops crypto tooling; works offline for GPG sign/verify.
- **Con:** Key sprawl; blind keyscan in CI is a MITM risk.
- **Trade-off:** Agent convenience vs exposure on shared bastions (`-A`).

## Comparison
- vs [[SSH]] client sessions: this note is key/trust helpers


### Use cases
- Pre-seeding bastion host keys in automation (with pinned fingerprints), rotat…
