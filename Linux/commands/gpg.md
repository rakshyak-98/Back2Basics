[[Commands]] [[keyrings]] [[apt package manager]] [[Authentication command]] [[apt config]] [[source list file]]

# gpg

> gpg (GNU Privacy Guard) encrypts, decrypts, signs, and verifies with OpenPGP keys — also how apt trusts third-party repos.

```txt
        gpg ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Know encrypt vs sign, armor, fingerprint verification for apt keyrings, and n…

## Sources
- [GnuPG Handbook](https://www.gnupg.org/gph/en/manual.html) — deep-dive
- [gpg(1)](https://man.archlinux.org/man/gpg.1) — overview

## Key Concepts
- **Public vs private:** Publish/export public; guard private.
- **Armor:** ASCII-safe encoding — not encryption by itself.
- **Fingerprint:** Out-of-band identity check before trust.
- **Detach sign:** Signature file beside the artifact.
- **Revocation:** Publish revoke if private key is lost/compromised.


- **Core:** OpenPGP operations on a keyring: encrypt to a recipient’s public key, decrypt…

## Technical Details
```bash
gpg --full-generate-key
gpg --list-keys
gpg --list-secret-keys --keyid-format=long
gpg --fingerprint <keyid>

gpg --armor --export <keyid> > public.asc
gpg --armor --export-secret-keys <keyid> > private.asc   # guard this
gpg --import public.asc

gpg --armor --encrypt --recipient 'you@example.com' -o out.asc plain.txt
gpg --decrypt out.asc

gpg --detach-sign file.txt
gpg --verify file.txt.sig file.txt

gpg --gen-revoke <keyid>
gpg --edit-key <keyid>

gpg --no-default-keyring --keyring /usr/share/keyrings/nginx.gpg --fingerprint
curl -fsSL https://example.com/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/example.gpg
```

| Symptom | Check | Fix |
|---------|-------|-----|
| NO_PUBKEY / apt signed-by fail | Keyring path/fingerprint | Install correct dearmored key |
| Can’t decrypt | Wrong private key | Import secret; check recipient |
| Git signing fails | `user.signingkey` | List secret keys; fix git config |
| Trust warning | Ultimate/unknown trust | `gpg --edit-key` trust; or explicit verify |

## Mistakes to Avoid
- **Mistake:** Emailing or committing private key armor
- **Mistake:** Skipping fingerprint checks when adding apt keys
- **Mistake:** Deleting `~/.gnupg` without revocation if the key was published

## Pros/Cons or Trade-offs
- **Pro:** Standard OpenPGP tool; works offline; apt integration pattern is clear.
- **Con:** UX complexity; key loss is catastrophic without revoke+backup plan.
- **Trade-off:** Long-lived personal keys vs short-lived signing certs where available.

## Comparison
- vs [[Authentication command]] SSH keys: different protocols


### Use cases
- Signing Git commits, verifying vendor release signatures, and installing a th…
