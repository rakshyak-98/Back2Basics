[[git merge]] [[Release cycle]] [[staff engineer]] [[Repro]]

# Code review

> Code review — a second engineer checks correctness, security, and clarity before a change merges.

## Interview Relevance
Shows engineering culture maturity: what you look for, how you give feedback, and how you keep reviews from blocking [[Release cycle]] without rubber-stamping.

## Sources
- [Google Engineering Practices — Code Review](https://google.github.io/eng-practices/review/) — deep-dive
- [Wikipedia — Code review](https://en.wikipedia.org/wiki/Code_review) — overview

## Core Definition
Code review is a human (or human+tool) inspection of a proposed change against standards: behavior, tests, security, operability, and maintainability — before it becomes the team’s long-term liability.

## Key Concepts
- **Correctness first:** Does it do what the ticket claims? Edge cases? Race conditions?
- **Design fit:** Right abstraction level; avoids drive-by refactors unrelated to the change.
- **Security & data:** AuthZ checks, injection, secrets, PII in logs.
- **Tests & [[Repro]]:** How will the next engineer prove this still works?
- **Tone:** Critique the diff, not the person; prefer concrete suggestions.

## Technical Details
Typical checklist (adapt per stack):
1. Intent clear from PR description / TL;DR.
2. Tests cover happy path + one failure mode.
3. No secrets; migrations are expand/contract safe.
4. Observability: logs/metrics for new failure modes.
5. Performance: N+1, unbounded loops, missing indexes called out.
6. Rollout: flag, canary, or documented rollback.

Tools accelerate (linters, SAST) but do not replace judgment on architecture and product risk.

## Real-World Applications
PR for a payment webhook: reviewer verifies signature check, idempotency, and that failures go to a DLQ — not only that TypeScript compiles.

## Pros/Cons or Trade-offs
- **Pro:** Catches bugs early; spreads knowledge; raises bar.
- **Con:** Slow queues; nitpick culture; large PRs that cannot be reviewed well.

## Comparison
vs pair programming: review is async and archival; pairing is sync. vs CI: automation checks mechanical rules; review checks intent and trade-offs. Related: [[staff engineer]] ownership of review quality.

## Mistakes to Avoid
- Approving without running or reading tests.
- Blocking on style that a formatter already owns.
- Mega-PRs (“LGTM” without understanding).
- Review as gatekeeping instead of shared quality ownership.
