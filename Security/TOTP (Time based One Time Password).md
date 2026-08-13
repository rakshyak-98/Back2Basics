[[Security]] [[Authentication terms]] [[JWT]] [[single-sign-on (SSO)]]

# TOTP (Time based One Time Password)

> TOTP — six-digit codes from a shared secret + current time (Authenticator apps); second factor after password.

---

## How it works

```txt
Enroll: server → secret → QR (otpauth://…) → app stores secret
Login:  user types 6 digits → server checks(secret, now) → ok / fail
```

| Piece | Meaning |
|-------|---------|
| **Secret** | Shared key (protect like a password) |
| **Time step** | Usually 30s |
| **Window** | Accept previous/next step for clock skew |
| **otpauth URI** | `otpauth://totp/Issuer:user?secret=…&issuer=…` |

---


## Configuration and commands

```js
const otplib = require('otplib')

const secret = otplib.authenticator.generateSecret()
const token = otplib.authenticator.generate(secret)
const ok = otplib.authenticator.check(userInputCode, secret)

// Persist secret encrypted at rest; show QR once at enrollment
```

| Knob | Why it matters |
|------|----------------|
| Window / skew | NTP drift causes false rejects |
| One-time use per step | Reject replay of same code in same 30s |
| Backup codes | Recovery when phone lost |
| Rate limit | Brute-force 6 digits still needs throttling |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Valid app code rejected | Server clock; window size | Sync NTP; widen window slightly |
| Codes work then stop | Secret truncated/re-encoded | Store raw Base32; don’t “fix” casing |
| QR won’t scan | Bad otpauth URI | Encode issuer/account; use standard URI |
| User locked out | Lost phone | Backup codes; admin reset + re-enroll |
| Same code accepted twice | No replay cache | Remember used code for that timestep |
| SMS fallback abused | SIM swap | Prefer TOTP/WebAuthn over SMS |

---


## Gotchas

> [!WARNING]
> **Secret in plaintext DB** — treat like password hashes; encrypt or HSM-wrap.

> [!WARNING]
> **QR on a shared screen** — anyone who photographed enrollment owns the factor.

> [!WARNING]
> **TOTP ≠ phishing-resistant** — real-time phishing can relay codes; prefer WebAuthn/passkeys for high assurance.

---


## When not to use

- **Passwordless high-security** — WebAuthn/passkeys beat TOTP.
- **Non-interactive machine authentication** — use mTLS or signed service tokens.
- **Offline airgap with no clock** — TOTP needs rough time sync.

---


## Related

[[Authentication terms]] [[JWT]] [[single-sign-on (SSO)]] [[yashcrypt]] [[HMAC (Hash based Message Authentication Codes)]]

## Sources

- [Wikipedia — TOTP](https://en.wikipedia.org/wiki/TOTP)
