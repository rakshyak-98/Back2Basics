[[Repro]] [[general]] [[README]] [[Code review]] [[Release cycle]]

# TL;DR

> TL;DR — put the outcome and key constraint first; details follow.

```txt
        TL;DR ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Communication skill reviews and staff promo packets reward executives who …

## Sources
- [Wikipedia — TL;DR](https://en.wikipedia.org/wiki/TL%3BDR) — overview
- [Google Engineering Practices — Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) — deep-dive

## Key Concepts
- **Answer first:** Decision, impact, or fix command in line one.
- **Constraint next:** What limits the solution (deadline, blast radius, SLO).
- **Details after:** Evidence, alternatives, links.
- **Audience:** On-call, reviewer, and exec need different depth — same first line.


- **Core:** TL;DR means “too long; didn’t read”

## Technical Details
| Context | First line |
|---------|------------|
| PR | What changed + why (risk) |
| Runbook | Fix command / rollback before theory |
| Chat/incident | “API 5xx from bad deploy; rolling back `api` now.” |
| Design doc | Recommendation + top trade-off |

- Pair with [[Repro]] when claiming a bug: TL;DR states the failure

## Mistakes to Avoid
- **Mistake:** Burying the rollback command under paragraphs of history
- **Mistake:** TL;DR that restates the title without a decision
- **Mistake:** Omitting the risk/constraint (“works” without “at what cost”)

## Pros/Cons or Trade-offs
- **Pro:** Respects reader time; surfaces decisions.
- **Con:** Over-compressed TL;DRs hide uncertainty — still link evidence.

## Comparison
- vs full narrative blog posts: opposite ordering. vs [[Repro]]: TL;DR communic…


### Use cases
- PR description: “Adds idempotency keys to checkout webhooks so Stripe retries…
