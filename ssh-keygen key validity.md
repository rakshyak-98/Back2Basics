[[SSH]] [[Authentication command]] [[gpg sign]]

# ssh-keygen key validity

> An SSH key works only if the server trusts the public key — generating a keypair alone does not grant access.





## Interview Relevance
Catches a common ops myth: “I ran ssh-keygen, why can’t I log in?” Validity is trust configuration (and optional certificate lifetime), not the private key existing on disk.

## Sources
- [OpenSSH manual — ssh-keygen](https://man.openbsd.org/ssh-keygen) — deep-dive
- [OpenSSH manual — sshd](https://man.openbsd.org/sshd) — overview (`authorized_keys`, certificates)

## Core Definition
A keypair is cryptographically sound when generated correctly; it is *authorized* only when the server (or a CA) accepts the public half for that user/host. Certificate keys add an explicit validity window via `-V`.

## Key Concepts
- **Trust store:** Usually `~/.ssh/authorized_keys` (or centralized CA / cloud metadata).
- **Private key secrecy:** Permissions (`600`), agent use, passphrase — compromise of private key = full impersonation.
- **Certificates vs plain keys:** `ssh-keygen -V` validity intervals apply to signing/inspecting **certificates**, not ordinary key generation.
- **Host keys:** Separate from user keys — verify `known_hosts` / TOFU or CA-signed host certs.

## Technical Details
```bash
ssh-keygen -t ed25519 -C "you@example.com"
ssh-copy-id user@host          # installs public key
ssh -i ~/.ssh/id_ed25519 user@host
```

Certificate example (concept): CA signs user public key with a time bound (`-V +1w`); `sshd` trusts the CA key, not each leaf forever.

Debug: `ssh -vvv`, server `auth.log` / `journalctl`, confirm public key line matches, correct user home, and `PubkeyAuthentication yes`.

## Real-World Applications
Onboarding: generate key locally, register public key in IdP or `authorized_keys`, never email private keys. Rotating access: remove old public keys; for certs, short `-V` windows limit blast radius.

## Pros/Cons or Trade-offs
- **Pro:** Strong auth without shared passwords; easy to revoke a single public key.
- **Con:** Key sprawl; lost private keys; misunderstanding of certificate `-V` vs “key expiry.”

## Comparison
vs password auth: keys resist phishing/reuse better when agent + passphrase used. vs cloud IAM roles / SSM: still SSH under the hood or replace SSH entirely. Related: [[SSH]], [[Authentication command]].

## Mistakes to Avoid
- Expecting `-V` on plain `ssh-keygen` keygen to “expire” a normal key.
- World-readable private keys or committing them to git.
- Installing the private key on the server instead of the public key.
- Forgetting SELinux/AppArmor or wrong home directory for `authorized_keys`.
