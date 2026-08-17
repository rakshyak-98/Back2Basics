[[ssh login]] [[ssh allow local system with key]] [[sshd config]] [[ssh agent]]

# SSH authentication

> SSH public-key authentication — the client signs a server challenge with its private key; the server verifies the signature with the matching public key in `authorized_keys`.

```txt
        SSH authentication ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want the challenge-sign-verify story, not “SSH uses keys,” plus …

## Sources
- [RFC 4252 — SSH Authentication Protocol](https://datatracker.ietf.org/doc/html/rfc4252) — deep-dive
- [OpenSSH manual — ssh](https://man.openbsd.org/ssh) — overview

## Key Concepts
- **Core:** Key-based SSH proves possession of a private key: the server sends a challeng…

## Technical Details
- Verification steps:

1. Client offers a public key.
2. Server looks it up in `authorized_keys` (and policy/`Match`).
3. Server issues a challenge; client signs with the private key.
4. Server decrypts/verifies with the public key — match ⇒ authenticated.

```bash
ssh -v user@host                 # verbose auth debug
ssh-keygen -lf ~/.ssh/id_ed25519.pub
cat ~/.ssh/authorized_keys
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Publickey denied | Key not in authorized_keys | Match `.pub` fingerprint on server |
| Wrong signature algorithm | Old server; new key type | Use ed25519 or rsa-sha2; check `PubkeyAcceptedAlgorithms` |
| Keyboard-interactive loop | PAM or 2FA module | Complete second factor; check server logs |
| Certificate expired | SSH certificate auth | Re-sign host/user cert with CA |

## Mistakes to Avoid
- **Mistake:** Sharing one private key across users or machines
- **Mistake:** Assuming the client can override server-disabled publickey
- **Mistake:** Ignoring algorithm mismatches between new clients and old `sshd`

## Pros/Cons or Trade-offs
- **Pro:** No password on the wire; easy automation with [[ssh agent]].
- **Con:** Stolen private keys are full credentials — passphrase + agent + per-user keys.
- **Con:** Misconfigured PAM/2FA looks like “keys broken.”

## Comparison
- vs password auth: keys scale better and avoid shared secrets; disable passwords after keys work.
- vs host-based auth: rare; key-per-user is the default staff-engineer path.


### Use cases
- Passwordless deploy users, bastion access, and Git over SSH.

- **Example:** `ssh -v` shows the client offering keys until one matches
