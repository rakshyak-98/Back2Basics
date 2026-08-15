[[Repro]] [[general]] [[README]] [[Code review]] [[Release cycle]]

# TL;DR

> TL;DR — put the outcome and key constraint first; details follow.

## Interview Relevance
Communication skill interviews and staff promo packets reward executives who lead with the answer. Same habit in PRs, runbooks, and incident chat.

## Sources
- [Wikipedia — TL;DR](https://en.wikipedia.org/wiki/TL%3BDR) — overview
- [Google Engineering Practices — Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) — deep-dive

## Core Definition
TL;DR means “too long; didn’t read” — a discipline of leading with the conclusion so busy readers get the decision, risk, or fix before narrative context.

## Key Concepts
- **Answer first:** Decision, impact, or fix command in line one.
- **Constraint next:** What limits the solution (deadline, blast radius, SLO).
- **Details after:** Evidence, alternatives, links.
- **Audience:** On-call, reviewer, and exec need different depth — same first line.

## Technical Details
Patterns:

| Context | First line |
|---------|------------|
| PR | What changed + why (risk) |
| Runbook | Fix command / rollback before theory |
| Chat/incident | “API 5xx from bad deploy; rolling back `api` now.” |
| Design doc | Recommendation + top trade-off |

Pair with [[Repro]] when claiming a bug: TL;DR states the failure; repro proves it.

## Real-World Applications
PR description: “Adds idempotency keys to checkout webhooks so Stripe retries do not double-charge. Flag: `checkout_idempotency` default off.” Reviewers decide faster; [[Code review]] quality rises.

## Pros/Cons or Trade-offs
- **Pro:** Respects reader time; surfaces decisions.
- **Con:** Over-compressed TL;DRs hide uncertainty — still link evidence.

## Comparison
vs full narrative blog posts: opposite ordering. vs [[Repro]]: TL;DR communicates; repro verifies. Related vault tone: [[general]], [[README]].

## Mistakes to Avoid
- Burying the rollback command under paragraphs of history.
- TL;DR that restates the title without a decision.
- Omitting the risk/constraint (“works” without “at what cost”).
