[[Asymmetrical Encryption]] [[PKI]] [[Root certificate]] [[openssl]] [[fingerprint]] [[DER]]

# Code signing

> Cryptographic signature on binaries, packages, or scripts — proves publisher identity and detects tampering since build.





## Interview Relevance
Supply-chain interviews cover who signs artifacts, how OS/store trust works, and what a broken chain or stolen signing key means.

## Sources
- [Wikipedia — Code signing](https://en.wikipedia.org/wiki/Code_signing) — overview
- [NIST SP 800-161 — Supply Chain Risk](https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final) — deep-dive

## Core Definition
Code signing attaches a cryptographic signature to binaries or packages so verifiers can check publisher identity and integrity.

## Key Concepts
**Code signing** binds artifact hash to **publisher private key**:

```txt
Build pipeline → hash artifact → sign with code-signing cert → attach signature
User OS/store  → verify with trusted CA / platform key → run or block
```

Platforms:
| Platform | Mechanism |
|----------|-----------|
| **Windows** | Authenticode (EV cert for kernel drivers) |
| **macOS/iOS** | Apple Developer ID + notarization |
| **Linux** | GPG on packages, Secure Boot shim |
| **npm/PyPI** | Sigstore, project keys (emerging) |

Failure modes: expired cert, revoked cert, unsigned sideload, supply-chain swap of unsigned artifact.

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

**Why timestamp authority:** signature valid after cert expires if TSA countersigned at sign time.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| "Unknown publisher" | Cert chain; expired | Renew cert; install intermediate |
| macOS Gatekeeper block | Notarization staple | Notarize; `xcrun stapler staple` |
| CI sign fails | HSM token; secret in env | Use cloud HSM; OIDC federated signing |
| Users still run malware | Unsigned build channel | Disable sideload; enforce policy |

## Real-World Applications
CI signs release artifacts; OS and app stores verify the publisher signature before install or update.

## Pros/Cons or Trade-offs
- **Pro:** Users and stores can verify publisher identity and detect tampering.
- **Con:** Internal-only scripts between trusted admins may use **checksum in git** instead of full code signing — still sign anything distributed to customers or endpoints.

## Comparison
- vs TLS server certs ([[PKI]]): signing authenticates an artifact publisher; TLS authenticates a network endpoint.
- vs [[fingerprint]]: fingerprint is a hash for human compare; code signing is a cryptographic signature chain.

## Mistakes to Avoid
- Signing ≠ sandbox — signed malware still runs if cert stolen — revocation matters.
- Private key on build agent — prime theft target — HSM/KMS signing.
- Re-signing changes hash — update release manifests and update servers.
