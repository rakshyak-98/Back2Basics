[[Repro]] [[general]] [[README]]

# TL;DR

> TL;DR — put outcome + key constraint first; details follow. In PRs: what changed and why. In runbooks: fix command before theory. In chat: answer the question in

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Patterns]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Anti-patterns]]
- [[#Related]]

## Mental model

Put **outcome + key constraint** first; details follow. In PRs: what changed and why. In runbooks: fix command before theory. In chat: answer the question in line one, then context.

## Standard config / commands

…

## Patterns

**PR / change**
> TL;DR: Add Redis cache on user profile read; 80% ↓ DB load; TTL 5m; invalidate on write.

**Incident**
> TL;DR: Payments 503 — Stripe webhook timeout; mitigated by raising nginx `proxy_read_timeout` to 60s; root fix in PR #882.

**Doc section**
> TL;DR: Use `set -euo pipefail` in bash scripts; `${VAR:?}` for required env.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## Anti-patterns

- TL;DR that's still three paragraphs
- Burying the verdict after background
- Using TL;DR without delivering a summary below

## Related

[[Repro]] [[README]] [[NOTES_STANDARD]]
