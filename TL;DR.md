[[Repro]] [[general]] [[README]]

# TL;DR

> **Too long; didn't read** — compressed summary up front; use in docs, PRs, and incident threads so busy readers get the decision in 10 seconds.

## Mental model

Put **outcome + key constraint** first; details follow. In PRs: what changed and why. In runbooks: fix command before theory. In chat: answer the question in line one, then context.

## Patterns

**PR / change**
> TL;DR: Add Redis cache on user profile read; 80% ↓ DB load; TTL 5m; invalidate on write.

**Incident**
> TL;DR: Payments 503 — Stripe webhook timeout; mitigated by raising nginx `proxy_read_timeout` to 60s; root fix in PR #882.

**Doc section**
> TL;DR: Use `set -euo pipefail` in bash scripts; `${VAR:?}` for required env.

## Anti-patterns

- TL;DR that's still three paragraphs
- Burying the verdict after background
- Using TL;DR without delivering a summary below

## Related

[[Repro]] [[README]] [[NOTES_STANDARD]]
