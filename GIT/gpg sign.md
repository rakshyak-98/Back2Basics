[[gpg]] [[git command]] [[git hook]]

# GPG sign (Git commits & tags)

> One-line: cryptographically **sign Git commits/tags** with your GPG key — proves authorship and integrity for supply-chain and release audit. **Fix "no secret key" before enabling signing in CI or globally.**

## Mental model

Git attaches an OpenPGP signature to commit or tag objects. Verifiers use your **public** key (`gpg --list-keys`) to confirm the signature matches your identity. Signing requires a **private** key in your agent's keyring — passphrase-protected by default.

```
git commit -S ──► gpg signs hash ──► signature embedded in commit
git log --show-signature ──► gpg --verify against trusted keys
```

| Error | Meaning |
|-------|---------|
| `gpg: no default secret key` | No private key selected / none installed |
| `gpg: signing failed: No secret key` | Key ID in git config doesn't match secret keyring |
| `gpg: signing failed: Inappropriate ioctl` | TTY/pinentry broken over SSH |

## Standard config / commands

**Generate key (if none):**

```bash
gpg --full-generate-key
# RSA 4096, expiry per policy, real name + email matching git

gpg --list-secret-keys --keyid-format=long
# sec   rsa4096/ABC123DEF456 2024-01-01 [SC]
#                ^^^^^^^^^^^^ long key ID for git config
```

**Git + GPG wiring:**

```bash
git config --global user.signingkey ABC123DEF456
git config --global commit.gpgsign true          # sign all commits
git config --global tag.gpgsign true             # sign tags

# Tell git which gpg binary (GPG 2.1+)
git config --global gpg.program gpg

# Sign one-off
git commit -S -m "feat: release prep"
git tag -s v1.2.0 -m "Release 1.2.0"
```

**Publish public key (GitHub/GitLab):**

```bash
gpg --armor --export ABC123DEF456
# Paste into GitHub → Settings → SSH and GPG keys
```

**Verify:**

```bash
git log --show-signature -1
git verify-commit HEAD
git verify-tag v1.2.0
```

**SSH signing (modern alternative — no GPG):**

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
```

See [[gpg]] for repo key verification (nginx packages, etc.) — different use case from commit signing.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `no default secret key` | `gpg --list-secret-keys` | Generate/import key; set `user.signingkey` |
| Wrong key used | `git config user.signingkey` | Match long ID from secret keyring |
| Passphrase loop over SSH | pinentry | `export GPG_TTY=$(tty)`; use `gpg-agent`; local sign |
| GitHub "Unverified" | Pubkey not uploaded | Export armor key to GitHub; email must match commit |
| CI can't sign | No secret in agent | Use bot key in CI secret store; or sign tags locally only |
| `error: gpg failed to sign` | `gpg.program` wrong | Point to `gpg` or `gpg2`; test `echo test \| gpg --clearsign` |

**Fix classic "No secret key":**

```bash
gpg --list-secret-keys --keyid-format=long    # must show sec line
git config --global user.signingkey <LONG_ID> # must match
gpg-agent --daemon                            # restart agent if stuck
export GPG_TTY=$(tty)
```

## Gotchas

> [!WARNING]
> **Key in git config but only public key imported** — signing needs **secret** key on that machine.

> [!WARNING]
> **Expired/revoked key** — old commits verify as expired. Plan rotation and GitHub key update.

> [!WARNING]
> **`commit.gpgsign true` globally** — rebases/amends re-sign constantly; ensure agent works or disable on throwaway branches.

> [!WARNING]
> **Subkeys vs primary** — git signing uses signing subkey if present; list with `--list-secret-keys`.

## When NOT to use

- **Internal-only repos with no audit requirement** — signing overhead may not pay off.
- **Replace code review** — signature proves key holder signed, not that code is safe.
- **Secrets in commits** — sign doesn't encrypt; use git-crypt/SOPS for confidentiality.

## Related

[[gpg]] [[git command]] [[git hook]] [[Authentication command]]
