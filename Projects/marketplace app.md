[[Projects]] [[TLS (Transport Layer Security)]] [[ACID]] [[IDOR]] [[JWT authentication]] [[gRPC]]

# marketplace app

> Two-sided marketplace architecture: **payments, trust, inventory, and dispute** boundaries — design checklist for staff reviews, not a build backlog.

---

## Mental model

```txt
Buyer ──► Catalog / Search ──► Cart ──► Checkout ──► Fulfillment
              ▲                              │
Seller ──► Listing / Inventory ──────────────┘
              │
         Trust layer: identity, reviews, escrow, moderation
         Money layer: split payouts, fees, refunds, tax
```

**Hard problems are orthogonal to CRUD:**
- **Double sale** of last unit (inventory concurrency)
- **Payment success, order create fail** (distributed transaction)
- **Seller payout vs chargeback window** (ledger timing)
- **Search ranking gaming** (trust/abuse)

Design for **eventual consistency** with explicit user-visible states — not one giant ACID transaction across Stripe + Postgres + search index.

---

## Standard config / commands

### Core bounded contexts

| Context | Owns | Integrates via |
|---------|------|----------------|
| Identity | users, roles, KYC status | [[JWT authentication]], SSO |
| Catalog | listings, media, categories | search indexer (async) |
| Inventory | stock, reservations | optimistic lock / row lock |
| Orders | state machine | events (`OrderPlaced`, …) |
| Payments | intents, captures, refunds | PSP webhooks (idempotent) |
| Payouts | seller balances, transfers | scheduled jobs + ledger |
| Trust | reviews, reports, bans | moderation queue |
| Notifications | email/SMS/push | outbox pattern |

### Order state machine (minimum)

```txt
created → payment_pending → paid → fulfilled → completed
                ↓               ↓
            cancelled      disputed → refunded
```

Persist transitions with **actor, reason, idempotency key** — support will replay history.

### Inventory reservation pattern

```sql
-- Short TTL hold during checkout (not final decrement)
UPDATE inventory
SET reserved = reserved + :qty
WHERE sku = :sku AND on_hand - reserved >= :qty;
-- Confirm on payment webhook; release on timeout job
```

### Payment webhook idempotency

```txt
POST /webhooks/stripe
  → verify signature
  → lookup event.id in processed_events (unique)
  → if new: update order + emit OrderPaid (same txn or outbox)
  → return 200 fast (heavy work async)
```

### Split payments (conceptual)

```txt
Charge buyer $100
  Platform fee $10 → platform balance
  Seller net $90   → pending_balance (T+N days)
Capture/refund partials adjust ledger entries — never overwrite amounts
```

### Search vs source of truth

```txt
Postgres = authoritative catalog
Elasticsearch/OpenSearch = query-optimized projection
Rebuild index from changelog; tolerate seconds lag with "syncing" UX if needed
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Oversold SKU | Reservation TTL, race logs | Pessimistic lock hot SKUs; extend hold on payment step |
| Paid order missing | Webhook 5xx / no idempotency | Replay webhooks; dead-letter queue; reconcile job |
| Seller not paid | Payout batch / KYC hold | Ledger report; manual adjustment with audit |
| Duplicate charges | Client double-submit | Idempotency-Key header on checkout API |
| Review bombing | Velocity by IP/account age | Rate limits; verified purchase only |
| Search shows delisted item | Index lag | Tombstone events; periodic full reindex |
| Tax wrong jurisdiction | Address vs IP vs nexus rules | Tax engine vendor; don't hand-roll VAT |

---

## Gotchas

> [!WARNING]
> **Treat PSP balance as source of truth for cash** — app ledger reconciles to Stripe daily; drift happens.

> [!WARNING]
> **[[IDOR]] on order IDs** — buyer/seller/admin scopes on every read; UUIDs aren't auth.

> [!WARNING]
> **Refunds after payout** — clawback from seller balance or platform absorbs — product policy + ledger design upfront.

> [!WARNING]
> **Multi-currency** — store minor units integer + ISO currency; never float.

> [!WARNING]
> **Guest checkout** — email verification before digital delivery; fraud rate higher.

---

## When NOT to use

- **Single merchant store** — Shopify/WooCommerce; skip two-sided payout complexity.
- **Classifieds (no payment on platform)** — trust/messaging only; narrower scope.
- **Real-time auction without ops** — sniping, shill bidding need dedicated fraud team.

---

## Related

[[ACID]] · [[connection pooling]] · [[TLS (Transport Layer Security)]] · [[Etherium]] · [[Progressive search functionality]] · [[Mermaid (DSL)]]
