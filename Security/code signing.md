[[Asymmetrical Encryption]] [[PKI]] [[Root certificate]] [[openssl]] [[fingerprint]] [[DER]]

# Code signing

> Cryptographic signature on binaries, packages, or scripts — proves publisher identity and detects tampering since build.

```txt
        Code signing ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Supply-chain reviews cover who signs artifacts, how OS/store trust works, …

## Sources
- [Wikipedia — Code signing](https://en.wikipedia.org/wiki/Code_signing) — overview
- [NIST SP 800-161 — Supply Chain Risk](https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final) — deep-dive

## Key Concepts
- **Note:** **Code signing** binds artifact hash to **publisher private key**:

```txt
- **Note:** Build pipeline → hash artifact → sign with code-signing cert → attach signatu…
- **Note:** User OS/store → verify with trusted CA / platform key → run or block
```

Platforms:
| Platform | Mechanism |
|----------|-----------|
| **Windows** | Authenticode (EV cert for kernel drivers) |
| **macOS/iOS** | Apple Developer ID + notarization |
| **Linux** | GPG on packages, Secure Boot shim |
| **npm/PyPI** | Sigstore, project keys (emerging) |

- **Note:** Failure modes: expired cert, revoked cert, unsigned sideload, supply-chain sw…


- **Core:** Code signing attaches a cryptographic signature to binaries or packages so ve…

## Technical Details
### Sign Windows (signtool — concept)

```powershell
signtool sign /fd SHA256 /a /tr http://timestamp.digicert.com /td SHA256 myapp.exe
signtool verify /pa myapp.exe
```

### Sign macOS

```bash
codesign --sign "Developer ID Application: Corp" --options runtime --timestamp myapp
spctl -a -vv myapp
xcrun notarytool submit myapp.zip --wait
```

### GPG sign release tarball

```bash
gpg --detach-sign --armor release.tar.gz
gpg --verify release.tar.gz.asc release.tar.gz
```

### Verify Authenticode / openssl CMS (generic)

```bash
openssl cms -verify -in signature.p7s -inform DER -content binary -noverify
```

- **Why timestamp authority:** signature valid after cert expires if TSA counte…

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| "Unknown publisher" | Cert chain; expired | Renew cert; install intermediate |
| macOS Gatekeeper block | Notarization staple | Notarize; `xcrun stapler staple` |
| CI sign fails | HSM token; secret in env | Use cloud HSM; OIDC federated signing |
| Users still run malware | Unsigned build channel | Disable sideload; enforce policy |

## Mistakes to Avoid
- **Mistake:** Signing ≠ sandbox
- **Mistake:** Private key on build agent — prime theft target — HSM/KMS signing
- **Mistake:** Re-signing changes hash

## Pros/Cons or Trade-offs
- **Pro:** Users and stores can verify publisher identity and detect tampering.
- **Con:** Internal-only scripts between trusted admins may use **checksum in git** instead of full code signing — still sign anything distributed to customers or endpoints.

## Comparison
- vs TLS server certs ([[PKI]]): signing authenticates an artifact publisher
- vs [[fingerprint]]: fingerprint is a hash for human compare


### Use cases
- CI signs release artifacts
