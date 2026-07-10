Idempotent request key validation prevents duplicate resource creation when a client retries a request (due to timeout, network failure, or duplicate submission) by using a unique key to detect and reject/duplicate repeat attempts.

**Problem it solves**
A client sends `POST /orders` to create a resource. The request succeeds server-side, but the response is lost (network drop, timeout). The client retries the same POST. Without protection, this creates a second, duplicate resource — a data integrity violation.

> [!NOTE]
> The key must be client-generated per logical operation, not server-generated, since the whole point is that the client can safely resend the same key across retries of the same logical request.

## Mechanism

1. Client generates a unique key (typically a UUID) per logical operation and sends it in a header, e.g.:

```
POST /orders
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
```

2. Server checks if that key has been seen before:
	- **Not seen**: process the request normally, store `(key, result, status)`, return the result.
	- **Seen, still processing**: return 409 Conflict or block/wait (request is in-flight).
	- **Seen, already completed**: return the stored response from the original request instead of re-executing the operation. Do not re-create the resource.

```sql
CREATE TABLE idempotency_keys (
  key             UUID PRIMARY KEY,
  request_hash    TEXT NOT NULL,      -- hash of request body, detects key reuse with different payload
  status          TEXT NOT NULL,      -- 'processing' | 'completed' | 'failed'
  response_body   JSONB,
  response_status INT,
  created_at      TIMESTAMPTZ DEFAULT now(),
  expires_at      TIMESTAMPTZ         -- TTL, e.g. 24h
);
```

> [!NOTE]
> - Store the request payload hash alongside the key. If the same key arrives with a different body, that's a client-side bug (key reused across different logical operations) — reject rather than silently applying one or the other.

