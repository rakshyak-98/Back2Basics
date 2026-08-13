<!-- note-strategy: operational -->
[[System Design]] [[Eventual consistency]] [[backpressure]] [[Real-time Subscription]]

# Food delivery

> Food-delivery design — geo-local marketplace: menu browse, sub-2s order accept, chef/driver state machine, async status fan-out at huge DAU.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Split read-heavy discovery (search/geo) from write-heavy order transactions; assignment and notifications are async workflows with clear cancellation rules.

```txt
User → API → Order service → (events) → Restaurant / Dispatch / Notify
                │
                └── durable order log (years of history)
```

| Constraint (example) | Design implication |
|----------------------|--------------------|
| ~100M DAU / multi-kQPS | Cache menus; shard orders |
| ~20 mi radius sort | Geo index / tiles |
| Cancel until cook starts | Explicit state machine |
| <2s accept | Sync persist + async rest |
| Status every change | Pub/sub / push |

---

## Standard config / commands

```txt
States: created → accepted → cooking → ready → picked_up → delivered
                         ↘ cancelled (only before cooking)
```

| Store | Role |
|-------|------|
| Catalog/search | Elastic/OpenSearch + CDN |
| Orders | Strongly consistent primary |
| Dispatch | Matching service + ETA models |
| Notifications | Queue → push/SMS |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Order accept >2s | DB lock / payment sync | Defer payment auth; optimize write path |
| Double charge | Retry without idempotency | Idempotency-Key on create |
| Driver never assigned | Dispatch lag / geo | Scale matcher; fallback pool |
| Cancel after cook | State guard missing | Enforce transitions server-side |
| Notification storm | Fan-out bug | Dedupe by order+state |

---

## Gotchas

> [!WARNING]
> **Menu cache vs price at checkout** — revalidate price on submit.

> [!WARNING]
> **Geo hot spots (stadium)** — surge capacity + demand shedding.

> [!WARNING]
> **Exactly-once delivery status** — users forgive delay more than wrong “delivered.”

---

## When NOT to use

- **Single restaurant POS** — don’t build a marketplace.
- **Interview without numbers** — always pin QPS/SLO first.
- **Copy Uber Eats wholesale** — scope to your actual constraints.

---

## Related

[[Eventual consistency]] [[backpressure]] [[Real-time Subscription]] [[database sharding]] [[Quorum]]
