[[stateless offset handling]] [[Real-time Subscription]] [[Horizontal vs Vertical Scaling]] [[cache system]]

# stateless

> A stateless service treats each request as independent — all context travels with the call (tokens, cursors, headers) so any replica can handle it and restarts do not strand in-memory session maps.

---

## What "stateless" means

The **application process** does not rely on local memory of prior requests for correctness. State may still live in databases, Redis, or the client — but not in a single pod's heap as the source of truth.

```txt
Client: GET /events?cursor=abc
Any replica → read durable store → response
(no per-pod map of connected users required for correctness)
```

| Property | Benefit |
|----------|---------|
| Client or store holds cursor | Horizontal scale behind load balancer without sticky sessions |
| Restart-safe | Kill pod; traffic shifts; no "lost" server-side session |
| Simple deploy | Rolling updates without draining custom connection state |

**Stateless is not "no state anywhere"** — it means state is **externalized** and **addressable** from any instance.

## Patterns

```http
GET /feed?cursor=eyJpZCI6MTIzfQ
Last-Event-ID: 42
Authorization: Bearer <token>
```

```javascript
app.get('/feed', async (req, res) => {
  const cursor = req.query.cursor ?? '0'
  const rows = await db.readAfter(cursor, 100)
  res.json({ items: rows, next: rows.at(-1)?.id })
})
```

| Knob | Why |
|------|-----|
| Signed opaque cursors | Prevent tampering with pagination tokens |
| Idempotent reads | Safe retries on GET |
| External session store | When you must remember server-side — Redis, not local `Map` |

## Connections versus stateless handlers

**WebSockets** hold connection state on one host — scale with shared pub/sub ([[Real-time Subscription]]) or accept reconnect with resume tokens ([[stateless offset handling]]). The *handler logic* can remain stateless if events are read from a shared log.

**JSON Web Tokens** carry claims client-side but revocation and session invalidation still need short time-to-live or denylist — "stateless authentication" has limits ([[Authentication web application]]).

## Failure signatures

| Symptom | Direction |
|---------|-----------|
| Requires sticky sessions | In-memory user map — move to Redis or token |
| Restart drops subscribers | Local connection registry — shared message bus |
| Duplicate or skipped pages | Cursor semantics wrong — document and test |
| Tampered page token | Sign with HMAC; validate server-side |

*When would you accept sticky sessions?* Legacy session affinity cheaper than refactor — plan migration to externalized state.

## Sources

- Twelve-Factor App — "VI. Processes" (execute as stateless processes).
- Google SRE Book — horizontal scaling and session affinity trade-offs.
