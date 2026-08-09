[[Payments]]

# razorpay integration

> razorpay integration — user clicks "Pay" on the Frontend.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** razorpay integration — plain job, how I run it, how I know it’s broken.


### **The High-Level Architecture Flow**
1. **User clicks "Pay"** on the Frontend.
2. **Frontend calls Backend** to create a new "Order".
3. **Backend calls Razorpay API** to generate a unique `order_id`, saves it to your database as "Pending", and sends it back to the Frontend.
4. **Frontend opens Razorpay Checkout** using that `order_id`.
5. **User completes payment** via the Razorpay UI.
6. **Razorpay sends success tokens** back to the Frontend.
7. **Frontend sends those tokens to Backend** for verification.
8. **Backend verifies the cryptographic signature** to ensure the payment is genuine, then updates the database to "Paid".
9. **(Safety Net) Razorpay Webhook fires** to your Backend in case the user closed their browser before Step 7.
### Workflow
1. **Customer Places an Order**
- Customer visits website/app
- Selects items to purchase
- Clicks pay button
- Creates a `transaction_id` or `checkout_id`

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **razorpay integration** | Core idea of this note | “I can explain razorpay integration without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Payments]]
