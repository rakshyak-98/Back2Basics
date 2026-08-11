[[Architectures]] [[System Design/Concurrent modification]]

# Idempotent-key

> Idempotency key lets a client safely retry a write — same key returns the first result, not a duplicate.

---

## Mental model

**Say it in one breath:** Client sends a unique key per logical op; server stores key→response and replays it on retry.

```txt
POST + Idempotency-Key
   │
   ├─ new key → process, store response
   ├─ in-flight → 409 / wait
   └─ seen done → return stored response (no re-create)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Idempotency-Key** | Client retry token | “UUID per checkout attempt.” |
| **Request hash** | Detect key reuse with new body | “Same key + different payload = 422.” |
| **TTL** | How long we remember | “24h is common for payments.” |
| **In-flight** | First request still running | “Don’t start a second charge.” |

---

## Standard config / commands

```http
POST /orders
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
```

```sql
CREATE TABLE idempotency_keys (
  key UUID PRIMARY KEY,
  request_hash TEXT NOT NULL,
  status TEXT NOT NULL, -- processing|completed|failed
  response_body JSONB,
  response_status INT,
  expires_at TIMESTAMPTZ
);
```

| Knob | Why it matters |
|------|----------------|
| Client-generated key | Server can’t invent it after a lost response |
| Hash of body | Stops accidental key reuse |
| TTL + purge | Table doesn’t grow forever |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate orders | Missing key / ignored | Require header; reject bare POST |
| 409 forever | Stuck `processing` | TTL reclaim; heartbeat |
| Wrong replay | Key reused for new body | Compare hash; 422 |
| Key missing on mobile retry | Client regenerated UUID | Persist key until success |

---

## Gotchas

> [!WARNING]
> **Server-generated keys don’t help** — the client must resend the *same* key after timeout.

> [!WARNING]
> **Only POST/PATCH that create side effects** — GET is already idempotent.

---

## When NOT to use

- **Pure reads** — no need.
- **Ops that must intentionally create many** — bulk create without keys is fine if duplicates are wanted.

## Related

[[System Architecture]] [[feature flag]] [[Service Layer]]
