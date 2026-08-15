[[System design]] [[API design]] [[Authentication web application]] [[marshalling]] [[event-driven]]

# Splitwise

> Splitwise-style systems track shared expenses in groups, derive who owes whom, and optionally simplify debts — a ledger and settlement tracker, not a payment processor unless integrated with one.

## Interview Relevance

Model balances as a graph of debts; idempotent expense writes; settle-up consistency.

## Sources

- Splitwise public product documentation — expense types and settlement semantics — overview
- Martin Kleppmann, *Designing Data-Intensive Applications* — ledger and event sourcing patterns for audit trails — deep-dive

## Key Concepts

- **Shared expenses:** group ledger of who paid / who owes.
- **Balance graph:** net debts; minimize settle-up transfers.
- **Idempotent writes:** retries must not double-charge an expense.
- **Consistency:** money-like invariants beat casual eventual merges.


## Technical Details

### Core entities

```txt
User creates expense $120 — Alice paid, split equally among Alice, Bob, Carol
  → Bob owes Alice $40, Carol owes Alice $40

Settlement: Bob pays Alice $40 → recorded → net edge zeroed
Simplify: if Alice owes Bob $30 and Bob owes Alice $50 → net Bob owes Alice $20
```

| Entity | Role |
|--------|------|
| User | Account, authentication |
| Group | Roommates, trip, household |
| Expense | Amount, payer, per-user splits, metadata |
| Balance | Derived net between users (per group) |
| Settlement | Payment recorded between two users |

Product requirements typically include: create groups, add or remove members, create and edit expenses, notify members, role-based access control (administrator versus member), settle debts.

## Application programming interface sketch

See [[API design]] for conventions:

```http
POST   /v1/groups
POST   /v1/groups/{id}/expenses
POST   /v1/groups/{id}/settlements
GET    /v1/groups/{id}/balances
```

### Split types

| Type | Rule |
|------|------|
| Equal | Amount divided by participant count |
| Exact | Fixed amounts per user (must sum to total) |
| Percentage | Percent per user |
| Shares | Weighted shares |

Store money as **integer minor units** (cents) — never floating point ([[marshalling]]).

## Balance calculation

```python
def balances(group_id):
    net = defaultdict(int)
    for exp in expenses(group_id):
        net[exp.payer_id] += exp.amount_cents
        for split in exp.splits:
            net[split.user_id] -= split.owed_cents
    for s in settlements(group_id):
        net[s.from_user] -= s.amount_cents
        net[s.to_user] += s.amount_cents
    return net
```

Persist **atomic expenses** as the audit trail; balances are derived (or materialized with careful invalidation).

## Debt simplification

Optional **minimum cash flow** on the net graph: repeatedly match the largest creditor with the largest debtor until balances zero. User experience may show both gross pairwise debts and simplified nets.

## Notifications and concurrency

Emit events (`expense_added`, `settlement_recorded`) to an async queue ([[event-driven]]) — do not block the expense POST on email or push delivery. Use **idempotency keys** on create to survive client retries.

Use database transactions or row locks per group when expense and settlement race ([[Concurrent modification]]).

## Authorization

Users read only groups they belong to. Only payer or group administrator edits an expense. JSON Web Token subject maps to `user_id` ([[Authentication web application]]).

## Scope limits

This pattern fits **informal expense sharing**. Enterprise accounts payable, tax invoicing, and high-frequency trading ledgers need different consistency and compliance models.

## Real-World Applications

Expense-sharing apps and lightweight social ledgers.


## Pros/Cons or Trade-offs

- **Pro:** Clear UX for multi-party balances.
- **Con:** Currency FX, partial settles, and dispute workflows complicate the model.
- **Trade-off:** simplify to pairwise nets vs full audit history.


## Comparison

- vs [[Food delivery]]: marketplace logistics vs shared-expense accounting.
- vs banking ledgers: Splitwise-style is social netting, not regulated core banking.


## Mistakes to Avoid

- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.

