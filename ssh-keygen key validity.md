[[SSH]] [[Authentication command]] [[gpg sign]]

# ssh-keygen key validity

> An SSH key works only if the server trusts the public key — generating a keypair alone does not grant access.

```txt
        ssh-keygen key val ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Catches a common ops myth: “I ran ssh-keygen, why can’t I log in?” Validity i…

## Sources
- [OpenSSH manual — ssh-keygen](https://man.openbsd.org/ssh-keygen) — deep-dive
- [OpenSSH manual — sshd](https://man.openbsd.org/sshd) — overview (`authorized_keys`, certificates)

## Key Concepts
- **Trust store:** Usually `~/.ssh/authorized_keys` (or centralized CA / cloud metadata).
- **Private key secrecy:** Permissions (`600`), agent use, passphrase
- **Certificates vs plain keys:** `ssh-keygen -V` validity intervals apply to signing/inspecting **certificates…
- **Host keys:** Separate from user keys — verify `known_hosts` / TOFU or CA-signed host certs.


- **Core:** A keypair is cryptographically sound when generated correctly

## Technical Details
```bash
ssh-keygen -t ed25519 -C "you@example.com"
ssh-copy-id user@host          # installs public key
ssh -i ~/.ssh/id_ed25519 user@host
```

- Certificate example (concept): CA signs user public key with a time bound (`-…

- Debug: `ssh -vvv`, server `auth.log` / `journalctl`, confirm public key line …

## Mistakes to Avoid
- **Mistake:** Expecting `-V` on plain `ssh-keygen` keygen to “expire” a normal…
- **Mistake:** World-readable private keys or committing them to git
- **Mistake:** Installing the private key on the server instead of the public k…
- **Mistake:** Forgetting SELinux/AppArmor or wrong home directory for `authori…

## Pros/Cons or Trade-offs
- **Pro:** Strong auth without shared passwords; easy to revoke a single public key.
- **Con:** Key sprawl; lost private keys; misunderstanding of certificate `-V` vs “key expiry.”

## Comparison
- vs password auth: keys resist phishing/reuse better when agent + passphrase u…


### Use cases
- Onboarding: generate key locally, register public key in IdP or `authorized_k…
