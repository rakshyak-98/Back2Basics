[[Architectures]] [[System Architecture]] [[frontend layered architecture]] [[Idempotent-key]]

# feature flag

> Feature flags turn code paths on/off remotely — ship dark, open to cohorts, kill fast.

```txt
        feature flag ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Feature flags show release-control maturity

## Sources
- [Martin Fowler — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) — deep-dive
- [LaunchDarkly — Feature flag best practices](https://docs.launchdarkly.com/guides/flags) — overview

## Key Concepts
```txt
Dashboard → Flag service → SDKs (poll/SSE)
                              ↓
                     if (flag) newPath else oldPath
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Flag** | Remote boolean/variant | “Checkout_v2 for 5% of users.” |
| **Targeting** | Who gets it | “User id, % rollout, plan tier.” |
| **Kill switch** | Instant off | “Disable without rollback.” |
| **Stale cache** | SDK holds old value | “Short TTL; listen for updates.” |

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Flag ignored | Wrong key / env | Match project + environment |
| Flip doesn’t propagate | SDK cache | Force refresh; lower TTL |
| Partial cohort weirdness | Sticky bucketing | Consistent hash on user id |
| “Temporary” flag forever | Code archaeology | Remove flag + dead path |

## Mistakes to Avoid
- **Mistake:** Flags are not security — hide UI, still enforce authz server-side
- **Mistake:** Combinatorial explosion

## Pros/Cons or Trade-offs
- **Trade-off:** configuration that rarely changes — environment variables / configuration files may be enough.
- **Trade-off:** Permanent product differences — that’s packaging/plans, not a forever flag.
