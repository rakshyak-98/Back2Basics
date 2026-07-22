[[DRY]] [[SOLID]] [[System design]] [[Design pattern]]

# KISS (Keep It Simple, Stupid)

> Prefer the simplest design that meets requirements — **complexity is a liability** with compound interest.

---

## Mental model

**KISS** pushes teams to choose **understandable** solutions over clever ones. Every abstraction, service boundary, and config flag has **operational cost** — on-call must debug it at 3 AM. Simple code is **easier to read, test, change, and delete**; complexity hides bugs and slows onboarding.

```txt
Requirement: send email on signup

KISS:  one function calls SMTP/API after DB insert
Not:   event bus + 3 services + saga for 10 users/day
```

| Symptom of over-complexity | KISS response |
|----------------------------|---------------|
| 5 layers for CRUD | Monolith module first |
| Generic plugin framework | Two concrete implementations max |
| Premature microservices | Modular monolith until scale proves split |
| Long methods | **Small named functions** — clarity ≠ fewer files |

KISS pairs with **[[DRY]]** — don't simplify by duplicating business rules; simplify **structure**.

---

## Standard config / commands

### Decision checklist (before adding complexity)

```txt
1. What is the smallest thing that works this sprint?
2. Can we delete it easily if wrong?
3. Will a mid-level engineer understand in 15 minutes?
4. Does complexity map to real scale (QPS, team size, compliance)?
5. Is the third similar use case here yet? (Rule of three for abstraction)
```

### Refactor toward KISS

```txt
Before: AbstractHandlerFactory → Strategy → Command
After:  switch on type with 4 clear functions (until N > 6)

Before: 6 microservices for MVP
After:  one deploy with modules; extract ingest when CPU bound
```

See [[Microservice]] for when split is justified.

### API surface KISS ([[API design]])

```txt
Expose: POST /orders { items, address }
Not:    POST /orders with 40 optional polymorphic fields day one
```

### Config KISS

```txt
Env vars for 5 knobs — not 200-line config framework on day one
Feature flags only for risky rollout, not every if-branch
```

### Code review prompts

```txt
"Can this be half the lines without lying?"
"What's the delete plan?"
"Will on-call need a diagram to fix this?"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No one owns service | Over-split architecture | Merge paths; clarify ownership |
| Bug in "framework" | Indirection depth | Inline hot path; add tests |
| Incidents hard to trace | Too many async hops | Sync where latency allows; correlation IDs |
| Slow feature delivery | Ceremony per change | Reduce layers; trunk-based |
| On-call runbook 20 pages | Operational complexity | Simplify deploy; reduce moving parts |
| "Works but nobody knows how" | Bus factor | Document or delete |

---

## Gotchas

> [!WARNING]
> **KISS ≠ sloppy** — simple still needs tests and error handling.

> [!WARNING]
> **Permanent temporary hacks** — KISS allows shortcuts; ticket the paydown.

> [!WARNING]
> **Confusing simple with familiar** — wrong tech "we know" can be complex in prod.

> [!WARNING]
> **Splitting methods into one-liners** — readability wins over line count rules.

> [!WARNING]
> **KISS against security** — simple auth must still be correct ([[JWT authentication]]).

---

## When NOT to use

- **Proven scale pain** — 10M QPS needs sharding, not bigger monolith wishful thinking.
- **Regulatory audit boundary** — DRM license service isolation is complexity worth paying ([[DRM]]).
- **Safety-critical systems** — formal verification may trump "simple" shortcuts.

---

## Related

[[DRY]] [[SOLID]] [[System design]] [[API design]] [[Design pattern]] [[Microservice]]
