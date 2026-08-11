[[Payments]]

# payment integration razorpay

> payment integration razorpay — payment capture in Razorpay is the process of confirming and securing a payment after it has been authorized. It ensures that…

---

## Mental model

**Say it in one breath:** payment integration razorpay — payment capture in Razorpay is the process of confirming and securing a payment after it has been authorized. It ensures that…

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
