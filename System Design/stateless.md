[[stateless offset handling]] [[Real-time Subscription]] [[Horizontal vs Vertical Scaling]] [[cache system]] [[Authentication web application]]

# stateless

> A stateless service treats each request as independent — context travels with the call (tokens, cursors, headers) so any replica can handle it and restarts do not strand in-memory session maps.

```txt
        stateless ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Externalize state for horizontal scale

## Sources
- Twelve-Factor App — “VI. Processes” — overview
- Google SRE Book — horizontal scaling / session affinity — overview

## Key Concepts
- **Process is stateless:** correctness does not depend on local prior-request memory.
- **State still exists:** DB, Redis, client — externalized and addressable.
- **Cursors/tokens:** pagination and auth travel with the request.
- **Connections ≠ handlers:** sockets may be sticky; logic can still read shared logs.

## Technical Details
```txt
Client: GET /events?cursor=abc
Any replica → durable store → response
```

| Property | Benefit |
|----------|---------|
| Client/store holds cursor | Scale without sticky sessions |
| Restart-safe | Kill pod; traffic shifts |
| Simple deploy | Rolling updates without draining custom maps |

```http
GET /feed?cursor=eyJpZCI6MTIzfQ
Last-Event-ID: 42
Authorization: Bearer <token>
```

- Sign opaque cursors (HMAC).
- External session store when needed — Redis, not local `Map`.
- WebSockets: shared pub/sub ([[Real-time Subscription]]) or resume tokens ([[s…
- JWT revocation still needs short TTL or denylist ([[Authentication web applic…

| Symptom | Direction |
|---------|-----------|
| Requires sticky sessions | Move map to Redis/token |
| Restart drops subscribers | Shared message bus |
| Dup/skipped pages | Fix cursor semantics |
| Tampered page token | HMAC validate |

## Mistakes to Avoid
- **Mistake:** Calling JWT auth fully stateless while ignoring revocation
- **Mistake:** Keeping the only subscriber registry in one pod’s memory
- **Mistake:** Unsigned cursors clients can forge

## Pros/Cons or Trade-offs
- **Pro:** Easy horizontal scale and rolling deploys.
- **Con:** External store latency; larger request metadata.
- **Trade-off:** sticky sessions (legacy speed) vs externalized state (scale).

## Comparison
- vs sticky sessions: affinity hides local state; brittle under failover.
- vs [[Horizontal vs Vertical Scaling]]: stateless unlocks horizontal app tier scale.


### Use cases
- Stateless API fleets behind LBs, mobile feeds with cursors, and twelve-factor…
