[[System Design]] [[distributed system]] [[Quorum]] [[cache system]]

# Eventual consistency

> Eventual consistency — replicas may disagree briefly after a write; if you stop writes, they converge to the same values.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** AP-leaning systems acknowledge quickly, replicate async, and heal with read repair / anti-entropy. Users may see stale data for a window.

```txt
Write → replica A (ack)
     ↘ async → replicas B,C  (later)
Read may hit B early → stale
```

| Pattern | Example |
|---------|---------|
| DNS TTL | Old IP until cache expires |
| Cache + DB | Invalidate/TTL |
| Multi-master | CRDTs / LWW |
| CQRS read models | Async projection |

---

## Standard config / commands

```txt
Client strategies
- Read-your-writes: sticky session / primary read
- Monotonic reads: session consistency tokens
- Tolerate stale: show “updating…” UX
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| User sees old profile | Replica lag / cache | Bypass cache; higher R; wait |
| Never converges | Conflict policy missing | LWW/CRDT/merge; repair job |
| “Lost” update | Concurrent writers | Version vectors; CAS |
| Hot key lag | Single partition overload | Shard; buffer |
| Billing mismatch | Wrong consistency tier | Stronger path for money |

---

## Gotchas

> [!WARNING]
> **Eventual ≠ “who cares”** — define the SLA window and conflict rule.

> [!WARNING]
> **Caches without invalidation** — eternal eventual.

> [!WARNING]
> **Money/inventory** — usually need stronger consistency or reservations.

---

## When NOT to use

- **Bank ledgers / unique inventory** — use strong consistency or explicit reservation.
- **Security policy flips** — don’t leave revoke eventually for long.
- **Single-node app** — you already have “immediate.”

---

## Related

[[Quorum]] [[distributed system]] [[cache system]] [[Concurrent modification]]
