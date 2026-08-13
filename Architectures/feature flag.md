<!-- note-strategy: operational -->
[[Architectures]] [[System Architecture]]

# feature flag

> Feature flags turn code paths on/off remotely — ship dark, open to cohorts, kill fast.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Wrap the new path in a check; a flag service (or configuration) decides who sees it without redeploying.

```txt
Dashboard → Flag service → SDKs (poll/SSE)
                              ↓
                     if (flag) newPath else oldPath
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Flag** | Remote boolean/variant | “Checkout_v2 for 5% of users.” |
| **Targeting** | Who gets it | “User id, % rollout, plan tier.” |
| **Kill switch** | Instant off | “Disable without rollback.” |
| **Stale cache** | SDK holds old value | “Short TTL; listen for updates.” |

---

## Standard config / commands

```js
if (featureFlags.isEnabled('new-checkout', { userId })) {
  showNewCheckout()
} else {
  showOldCheckout()
}
```

| Knob | Why it matters |
|------|----------------|
| Default when service down | Fail closed vs open — pick per flag |
| Server + client checks | Don’t trust UI-only gates for authz |
| Cleanup tickets | Flags rot into permanent branches |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Flag ignored | Wrong key / env | Match project + environment |
| Flip doesn’t propagate | SDK cache | Force refresh; lower TTL |
| Partial cohort weirdness | Sticky bucketing | Consistent hash on user id |
| “Temporary” flag forever | Code archaeology | Remove flag + dead path |

---

## Gotchas

> [!WARNING]
> **Flags are not security** — hide UI, still enforce authz server-side.

> [!WARNING]
> **Combinatorial explosion** — too many overlapping flags = untestable matrix.

---

## When NOT to use

- **configuration that rarely changes** — environment variables / configuration files may be enough.
- **Permanent product differences** — that’s packaging/plans, not a forever flag.

## Related

[[System Architecture]] [[frontend layered architecture]] [[Idempotent-key]]
