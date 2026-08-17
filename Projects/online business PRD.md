[[Projects]] [[marketplace app]] [[ecommerce-platform-architecture]]

# Product Requirements Document (PRD)

> Written agreement on what to build, for whom, and how you will know it worked — strategy and scope before sprint noise.

```txt
        Product Requiremen ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers (PM/eng) look for problem statement, personas, must-haves vs out…

## Sources
- [SVPG — Product requirements](https://www.svpg.com/product-requirements/) — overview
- [Wikipedia — Product requirements document](https://en.wikipedia.org/wiki/Product_requirements_document) — overview

## Technical Details
- Lightweight PRD skeleton:

1. Context and problem
2. Goals / non-goals
3. Users and stories
4. Scope (MVP)
5. Metrics
6. Risks and open questions
7. Rollout / analytics

- Hand to engineering with enough edge cases (payments, empty states, permissio…

## Mistakes to Avoid
- **Mistake:** Specifying UI pixels without user outcome or metrics
- **Mistake:** No non-goals — everything looks mandatory
- **Mistake:** Writing PRDs after the code ships (retroactive fiction)

## Pros/Cons or Trade-offs
- **Pro:** Aligns teams; reduces thrash mid-sprint.
- **Con:** Over-long PRDs rot; keep them living and short.

## Comparison
- vs tech design doc: PRD is product/outcome; TDD is how the system is built.
- vs backlog tickets: PRD sets direction; tickets schedule slices.


### Use cases
- Kick off a marketplace or AI feature with a PRD so design, eng, and stakehold…

- **Example:** Stakeholder asks for five integrations in v1
