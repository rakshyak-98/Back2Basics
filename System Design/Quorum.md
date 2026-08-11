[[System Design]] [[Raft]] [[distributed system]] [[Eventual consistency]]

# Quorum

> Quorum — minimum votes (nodes) that must agree before a read/write counts; trades availability against consistency.

---

## Mental model

**Say it in one breath:** In a cluster of `N`, pick `W` ack for writes and `R` for reads so `R + W > N` ⇒ overlapping nodes ⇒ you see the latest write (common Dynamo-style rule).

```txt
N=3 replicas
W=2, R=2  → R+W=4 > 3 → strong-ish read-your-writes
W=1, R=1  → fast, stale reads possible
```

| Term | Meaning |
|------|---------|
| **N** | Replica count |
| **W** | Write acks required |
| **R** | Read responses required |
| Majority | `floor(N/2)+1` (Raft elections) |

---

## Standard config / commands

```txt
# Cassandra-style mental model
WRITE CONSISTENCY QUORUM
READ  CONSISTENCY QUORUM
# MongoDB: writeConcern / readConcern
# etcd/Raft: majority implicit
```

| Choice | Effect |
|--------|--------|
| W=N, R=1 | Durable writes; reads may miss if not careful |
| W=1, R=N | Fast write; expensive consistent read |
| Majority | Survives 1 failure in 3 |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Writes timeout | W too high / node down | Lower W carefully; repair nodes |
| Stale reads | R+W ≤ N | Raise R or W |
| Split brain fear | Even N / no fencing | Prefer odd N; Raft |
| Hot key | Same partition | Re-shard; cache |
| “Quorum lost” | Majority offline | Restore nodes; don’t accept writes |

---

## Gotchas

> [!WARNING]
> **R+W>N assumes no bit-rot / clock games** — still need repair (read repair, anti-entropy).

> [!WARNING]
> **Quorum ≠ Raft** — quorum is a count rule; Raft is a consensus protocol using majority.

> [!WARNING]
> **Client-side quorum without membership** — wrong N during reconfig.

---

## When NOT to use

- **Single-node DB** — no quorum to take.
- **Apportioned pure AP shopping carts** — may choose W=1 intentionally.
- **Global sync low-latency UX** — quorum across regions hurts; use local + async.

---

## Related

[[Raft]] [[distributed system]] [[Eventual consistency]] [[Distributed computing]]
