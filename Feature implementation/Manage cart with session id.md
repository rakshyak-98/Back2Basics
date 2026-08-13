[[Feature implementation]] [[ExpressJS]] [[cookies]] [[cookies lifecycle]]

# Manage cart with session id

> Guest shopping carts bind to a server-side session identifier — persist cart items in session storage or a database keyed by session until the user logs in and merges into an account cart.

---

## Session-backed cart flow

```txt
Browser session cookie → session ID → cart storage (memory / Redis / DB)
Login → merge guest cart into user cart → invalidate or reuse session
```

Unauthenticated users need a stable session without requiring registration. Authenticated users should use `userId` as the primary cart key.

---

## Backend structure

```plaintext
/backend
├── controllers
│   ├── cartController.js       # add, remove, view
│   └── authController.js       # login, registration
├── models
│   ├── Cart.js                 # session or user keyed
│   └── User.js
├── routes
│   ├── cartRoutes.js
│   └── authRoutes.js
├── sessions
│   └── sessionManager.js       # storage and expiration
├── utils
│   └── sessionUtils.js
├── app.js
└── .env                        # session secret
```

| Decision | Trade-off |
|----------|-----------|
| In-memory session | Fast; lost on restart |
| Redis session | Survives restarts; shared across nodes |
| DB-backed cart | Persistent; more queries |

Use `express-session` with a secure cookie (`httpOnly`, `sameSite`) and a strong secret in `.env`. Set session TTL aligned with cart abandonment policy.

---

## Merge on login

1. Read guest cart from session ID.
2. Load user cart from `userId`.
3. Merge line items (dedupe SKUs, sum quantities).
4. Save merged cart under `userId`.
5. Clear guest session cart.

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cart empty after deploy | In-memory sessions | Redis or DB backing |
| Cart lost on login | No merge step | Implement merge in auth handler |
| Duplicate items | Merge logic missing | Dedupe by product ID |
| Session fixation | Reuse session after login | Regenerate session ID on auth |

---

## Related

[[Feature implementation]] · [[cookies lifecycle]] · [[cookies configuration]]
