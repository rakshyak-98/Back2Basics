[[System Design]] [[stateless offset handling]] [[Real-time Subscription]] [[Streaming]]

# stateless

> Stateless service — each request carries the context it needs; the server forgets you between calls (easy to scale and restart).

---

## Mental model

**Say it in one breath:** No sticky in-memory session. Client sends cursor/token/offset; any replica can serve. Restarts don’t lose “who was connected” because that wasn’t stored.

```txt
Client: GET /events?cursor=abc
Any pod → read store → stream → response
(no local map of clients)
```

| Trait | Implication |
|-------|-------------|
| Client holds cursor | `Last-Event-ID`, Kafka offset, page token |
| Horizontal scale | LB without affinity |
| Restart-safe | Pure functions of input + durable store |

---

## Standard config / commands

```http
GET /stream HTTP/1.1
Last-Event-ID: 42
```

```js
// Handler uses only request + DB — no global clients Map
app.get('/feed', async (req, res) => {
  const cursor = req.query.cursor ?? '0'
  const rows = await db.readAfter(cursor, 100)
  res.json({ items: rows, next: rows.at(-1)?.id })
})
```

| Knob | Why |
|------|-----|
| Cursor integrity | Sign/encrypt tokens if opaque |
| Idempotent reads | Retries safe |
| Externalize state | Redis/DB if you *must* remember |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate/skip events | Cursor not advanced correctly | Document cursor semantics; tests |
| Sticky session required | In-memory user state | Move state to Redis/JWT/DB |
| Restart drops users | Local connection map | Accept drop or shared pub/sub |
| Cursor tampering | Unsigned page tokens | Sign HMAC; server-side validate |
| Hot partition | Bad shard key on cursor | Re-key; fan-out |

---

## Gotchas

> [!WARNING]
> **WebSockets aren’t automatically stateful forever** — connection is state; scale with shared broker.

> [!WARNING]
> **“Stateless JWT” still has revoke/state problems** — short TTL or denylist.

> [!WARNING]
> **Hidden state in files /temp** — breaks multi-instance.

---

## When NOT to use

- **Long interactive workflows with huge server-side drafts** — store draft ids server-side.
- **Strong presence (“who’s online”)** — needs shared state.
- **Exactly-once local buffers** — you’ll invent a store anyway ([[stateless offset handling]]).

---

## Related

[[stateless offset handling]] [[Real-time Subscription]] [[JWT]] [[cache system]]
