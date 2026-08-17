[[Security]] [[Authentication terms]] [[JWT]] [[single-sign-on (SSO)]] [[yashcrypt]] [[HMAC (Hash based Message Authentication Codes)]]

# TOTP (Time based One Time Password)

> TOTP — six-digit codes from a shared secret + current time (Authenticator apps); second factor after password.

```txt
        TOTP (Time based O ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** MFA reviews: shared secret + time step, clock skew windows, and enrollment…

## Sources
- [RFC 6238 — TOTP](https://www.rfc-editor.org/rfc/rfc6238) — deep-dive
- [RFC 4226 — HOTP](https://www.rfc-editor.org/rfc/rfc4226) — overview

## Key Concepts
```txt
- **Note:** Enroll: server → secret → QR (otpauth://…) → app stores secret
- **Note:** Login: user types 6 digits → server checks(secret, now) → ok / fail
```

| Piece | Meaning |
|-------|---------|
| **Secret** | Shared key (protect like a password) |
| **Time step** | Usually 30s |
| **Window** | Accept previous/next step for clock skew |
| **otpauth URI** | `otpauth://totp/Issuer:user?secret=…&issuer=…` |


- **Core:** TOTP produces short numeric codes from a shared secret and the current time s…

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Valid app code rejected | Server clock; window size | Sync NTP; widen window slightly |
| Codes work then stop | Secret truncated/re-encoded | Store raw Base32; don’t “fix” casing |
| QR won’t scan | Bad otpauth URI | Encode issuer/account; use standard URI |
| User locked out | Lost phone | Backup codes; admin reset + re-enroll |
| Same code accepted twice | No replay cache | Remember used code for that timestep |
| SMS fallback abused | SIM swap | Prefer TOTP/WebAuthn over SMS |

## Mistakes to Avoid
- **Mistake:** Secret in plaintext DB
- **Mistake:** QR on a shared screen
- **Mistake:** TOTP ≠ phishing-resistant

## Pros/Cons or Trade-offs
- **Pro:** Offline second factor with broad authenticator-app support.
- **Con:** Passwordless high-security — WebAuthn/passkeys beat TOTP.
- **Con:** Non-interactive machine authentication — use mTLS or signed service tokens.
- **Con:** Offline airgap with no clock — TOTP needs rough time sync.

## Comparison
- vs SMS OTP: TOTP is offline and phishing-resistant-er than SMS (still phishable UX).
- vs WebAuthn: prefer hardware-backed MFA when available; TOTP is the common app factor.


### Use cases
- Authenticator-app MFA at login after password
