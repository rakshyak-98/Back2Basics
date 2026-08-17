[[Projects]] [[ecommerce-platform-architecture]] [[ACID]] [[JWT authentication]] [[Security/IDOR]] [[Payment gateway]]

# Marketplace app

> Two-sided marketplace: buyers and sellers share catalog and checkout — hard parts are inventory races, payments, payouts, and trust — not CRUD screens.





## Interview Relevance
Staff interviews probe double-sale prevention, webhook idempotency, payout vs chargeback windows, and explicit order state machines.

## Sources
- [Stripe — Webhooks best practices](https://stripe.com/docs/webhooks/best-practices) — deep-dive
- [Wikipedia — Online marketplace](https://en.wikipedia.org/wiki/Online_marketplace) — overview

## Key Concepts
- **Bounded contexts:** identity, catalog, inventory, orders, payments, payouts, trust, notifications.
- **Inventory reservation:** short TTL hold at checkout → confirm on pay, release on timeout.
- **Payment webhooks:** verify signature; store `event.id` uniquely; return 200 fast.
- **Trust layer:** KYC, reviews, moderation, escrow — orthogonal to listing CRUD.
- **Eventual consistency:** user-visible states beat fake cross-system ACID.

## Technical Details
```txt
Buyer ──► Catalog/Search ──► Cart ──► Checkout ──► Fulfillment
Seller ──► Listing/Inventory ───────────────────────┘
Trust: identity, reviews, escrow · Money: splits, fees, refunds
```

Order states (minimum):

```txt
created → payment_pending → paid → fulfilled → completed
                ↓               ↓
            cancelled      disputed → refunded
```

```sql
UPDATE inventory
SET reserved = reserved + :qty
WHERE sku = :sku AND on_hand - reserved >= :qty;
```

## Real-World Applications
Checkout reserves stock, creates payment intent, webhook marks paid and emits `OrderPaid` via outbox; payout job settles sellers after the chargeback window.

**Example:** Two buyers hit the last unit — reservation `WHERE` clause ensures only one hold succeeds.

## Pros/Cons or Trade-offs
- **Pro:** Explicit states make support and disputes workable.
- **Con:** More moving parts than a single-vendor storefront.

## Comparison
- vs single-vendor ecommerce: marketplace adds seller payouts, KYC, and abuse surfaces.
- vs [[ecommerce-platform-architecture]]: marketplace is the product shape on top of platform patterns.

## Mistakes to Avoid
- Decrementing stock only in the UI without a transactional reservation.
- Trusting webhooks without signature checks and idempotency keys.
- Paying sellers before chargeback/dispute windows close without a ledger plan.
