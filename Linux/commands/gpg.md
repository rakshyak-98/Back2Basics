[[commands]] [[keyrings]] [[apt package manager]] [[Authentication command]]

# gpg

> gpg (GNU Privacy Guard) encrypts, decrypts, signs, and verifies with OpenPGP keys — also how apt trusts third-party repos.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#APT keyrings (dearmor)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** public key encrypts / verifies; private key decrypts / signs; ASCII armor is the portable text form (`.asc`).

```txt
plaintext ──encrypt(+recipient pubkey)──► ciphertext
ciphertext ──decrypt(your privkey)──► plaintext
file ──sign(priv)──► signature; verify(pub)
armor ◄──► binary   (ASCII-safe email/git/apt)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Armor (`-a`)** | Base64-ish text form | “Safe to paste; ends with `.asc`.” |
| **Dearmor** | Text → binary keyring | “apt `signed-by=` wants a binary keyring file.” |
| **Recipient (`-r`)** | Whose pubkey encrypts | “Only their private key opens it.” |
| **Detach sign** | Signature beside file | “Verify integrity without rewriting the file.” |
| **Keyring path** | Isolated trust store | “`--no-default-keyring --keyring …` for apt keys.” |

---

## Standard config / commands

```bash
gpg --full-generate-key
gpg --list-keys
gpg --list-secret-keys --keyid-format=long
gpg --fingerprint <keyid>

# Export / import
gpg --armor --export <keyid> > public.asc
gpg --armor --export-secret-keys <keyid> > private.asc   # guard this
gpg --import public.asc

# Encrypt / decrypt
gpg --armor --encrypt --recipient 'you@example.com' -o out.asc plain.txt
gpg --decrypt out.asc

# Sign / verify
gpg --detach-sign file.txt
gpg --verify file.txt.sig file.txt
gpg --clear-sign file.txt

# Revocation
gpg --gen-revoke <keyid>
gpg --edit-key <keyid>          # adduid, expire, trust, …
gpg --delete-secret-keys <id>
gpg --delete-keys <id>
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `no valid OpenPGP data` | HTML error page / wrong URL | `file` the download; fix mirror |
| Can’t decrypt | Wrong recipient / missing secret | `list-secret-keys`; import private |
| apt `NO_PUBKEY` | Key not in keyring | Dearmor into `/etc/apt/keyrings` + `signed-by=` |
| Signature bad after edit | Detached sig for old bytes | Re-sign after change |
| Agent passphrase loops | pinentry / TTY | `export GPG_TTY=$(tty)`; check pinentry |

---

## APT keyrings (dearmor)

```bash
# Verify a vendor keyring fingerprint
gpg --no-default-keyring --keyring /usr/share/keyrings/nginx.gpg --fingerprint

# Compare to official download
gpg --no-default-keyring --keyring /usr/share/keyrings/nginx.gpg --export > localkey.gpg
curl -fsSL https://nginx.org/keys/nginx_signing.key -o officialkey.gpg
gpg --dearmor -o officialkey.gpg.gpg officialkey.gpg
diff -s localkey.gpg officialkey.gpg.gpg

# Modern apt install pattern
curl -fsSL https://example.com/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/example.gpg
```

Armor = human-readable OpenPGP text. Dearmor = back to binary for `signed-by=` in sources.list.

---

## Gotchas

> [!WARNING]
> **Never email private keys** — armor doesn’t mean safe; it means text-shaped.

> [!WARNING]
> **Deleting `~/.gnupg` is irreversible** without backups — revoke first if the key was published.

> [!WARNING]
> **apt key in the old global trusted.gpg** — prefer `/etc/apt/keyrings` + per-source `signed-by=`.

---

## When NOT to use

- **TLS for HTTPS APIs** — certificates / ACME.
- **SSH user authentication** — [[SSH]] / [[Authentication command]].
- **Password hashing for accounts** — `/etc/shadow` via `passwd`.

---

## Related

[[Authentication command]] [[keyrings]] [[apt package manager]] [[apt configuration]] [[commands]]
