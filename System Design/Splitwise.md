[[System design]] [[API design]] [[Authentication web application]] [[Distributed computing]]

# Splitwise

> Expense-sharing system design — **groups, balances, debt simplification, notifications**; classic interview + real fintech patterns.

---

## Mental model

**Splitwise-like** apps track **who paid** and **who owes whom** in **groups**. Core insight: store **atomic expenses** (who paid, split among whom) then **derive balances**; optionally **simplify debts** so A→B→C becomes A→C. Not a payment processor — **ledger + settlement tracking** unless integrated with Stripe/UPI.

```txt
User creates expense $120, A paid, split A/B/C equally
  → B owes A $40, C owes A $40

Settlement: B pays A $40 → mark settled → balances zero for that edge
Simplify: if A owes B $30 and B owes A $50 → net B owes A $20
```

| Entity | Purpose |
|--------|---------|
| **User** | Account, auth |
| **Group** | Roommates, trip |
| **Expense** | Amount, payer, splits, metadata |
| **Balance** | Derived net between pair (or per group) |
| **Settlement** | Payment recorded between users |

Requirements from product: add/remove/update user; create group; add members; notify members; create expense; settle debt; **RBAC** (admin vs member).

---

## Standard config / commands

### API sketch ([[API design]])

```txt
POST   /v1/users
POST   /v1/groups                    { name, member_ids[] }
POST   /v1/groups/{id}/members       { user_id }
DELETE /v1/groups/{id}/members/{uid}
POST   /v1/groups/{id}/expenses      { payer_id, amount, splits[] }
POST   /v1/groups/{id}/settlements   { from_user, to_user, amount }
GET    /v1/groups/{id}/balances      → simplified net per user
GET    /v1/users/{id}/notifications
```

### Expense split types

```txt
EQUAL       amount / N
EXACT       fixed amounts per user (must sum to total)
PERCENTAGE  % per user
SHARES      weighted shares
```

### DB schema (normalized)

```sql
expenses(id, group_id, payer_id, amount_cents, currency, note, created_at)
expense_splits(expense_id, user_id, owed_cents)
settlements(id, group_id, from_user, to_user, amount_cents, created_at)
-- Balances computed, not stored, OR materialized view refreshed on write
```

Store money as **integer cents** — never float ([[marshalling]] lesson).

### Balance calculation (per group)

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

### Debt simplification (min-cash-flow / net graph)

```txt
1. Compute net balance per user (+ creditor / - debtor)
2. Greedy: match max creditor with max debtor
3. Repeat until zeros
Optional — show unsimplified pair debts for transparency
```

### Notifications

```txt
Events: expense_added, member_added, settlement_recorded
Channels: push, email (async queue — don't block POST /expenses)
Idempotent notification delivery per event_id
```

### Auth / RBAC

```txt
User can only read groups they belong to
Only payer or admin can edit expense
JWT sub = user_id ([[JWT authentication]])
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Balances don't zero after settle | Partial settlement math | Validate amount ≤ owed |
| Split sum ≠ expense | Validation skipped | Reject POST if splits mismatch |
| User sees other group | Missing authz filter | group_id membership check |
| Duplicate expenses | Client retry | Idempotency-Key on POST |
| Notification spam | One event per split | Batch "A added expense" once |
| Currency mix | FX not in scope | One currency per group MVP |
| Simplify confuses users | UX | Show both gross and net |

---

## Gotchas

> [!WARNING]
> **Storing derived balances without expense audit** — can't reconcile disputes.

> [!WARNING]
> **Float dollars** — 0.1 + 0.2 bugs; integer cents only.

> [!WARNING]
> **Deleting user with history** — soft-delete; preserve ledger.

> [!WARNING]
> **Concurrent expense + settle** — transaction isolation or row locks on group.

> [!WARNING]
> **Splitwise ≠ bank transfer** — clarify "recorded settlement" vs actual payment.

---

## When NOT to use

- **Enterprise AP/AR** — use real accounting ERP; tax/invoicing rules differ.
- **High-frequency trading ledger** — different consistency/latency model.
- **Single-user budget app** — no group balance graph needed.

---

## Related

[[System design]] [[API design]] [[Authentication web application]] [[marshalling]] [[event-driven]] [[Quorum]]
