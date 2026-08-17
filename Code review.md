[[git merge]] [[Release cycle]] [[staff engineer]] [[Repro]]

# Code review

> Code review — a second engineer checks correctness, security, and clarity before a change merges.

```txt
        Code review ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shows engineering culture maturity: what you look for, how you give feedback,…

## Sources
- [Google Engineering Practices — Code Review](https://google.github.io/eng-practices/review/) — deep-dive
- [Wikipedia — Code review](https://en.wikipedia.org/wiki/Code_review) — overview

## Key Concepts
- **Core:** Code review is a human (or human+tool) inspection of a proposed change agains…

## Technical Details
- Typical checklist (adapt per stack):

1. Intent clear from PR description / TL;DR.
2. Tests cover happy path + one failure mode.
3. No secrets; migrations are expand/contract safe.
4. Observability: logs/metrics for new failure modes.
5. Performance: N+1, unbounded loops, missing indexes called out.
6. Rollout: flag, canary, or documented rollback.

- Tools accelerate (linters, SAST) but do not replace judgment on architecture …

## Mistakes to Avoid
- **Mistake:** Approving without running or reading tests
- **Mistake:** Blocking on style that a formatter already owns
- **Mistake:** Mega-PRs (“LGTM” without understanding)
- **Mistake:** Review as gatekeeping instead of shared quality ownership

## Pros/Cons or Trade-offs
- **Pro:** Catches bugs early; spreads knowledge; raises bar.
- **Con:** Slow queues; nitpick culture; large PRs that cannot be reviewed well.

## Comparison
- vs pair programming: review is async and archival


### Use cases
- PR for a payment webhook: reviewer verifies signature check, idempotency, and…
