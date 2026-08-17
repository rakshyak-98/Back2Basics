[[Projects]] [[marketplace app]] [[ecommerce-platform-architecture]]

# Product Requirements Document (PRD)

> Written agreement on what to build, for whom, and how you will know it worked — strategy and scope before sprint noise.





## Interview Relevance
Interviewers (PM/eng) look for problem statement, personas, must-haves vs out-of-scope, metrics, and explicit non-goals — not a feature laundry list.

## Sources
- [SVPG — Product requirements](https://www.svpg.com/product-requirements/) — overview
- [Wikipedia — Product requirements document](https://en.wikipedia.org/wiki/Product_requirements_document) — overview

## Recall Cues
- Why do interviewers care about Interviewers (PM/eng) look for problem statement, personas, must-haves vs out-of-scope, metrics, and explicit non-goals — not a feature laundry list?
- What is step 1: Context and problem?
- What is step 2: Goals / non-goals?
- What is step 3: Users and stories?
- What is step 4: Scope (MVP)?
- What is step 5: Metrics?
- What is step 6: Risks and open questions?
- What is step 7: Rollout / analytics?

## Technical Details
Lightweight PRD skeleton:

1. Context and problem
2. Goals / non-goals
3. Users and stories
4. Scope (MVP)
5. Metrics
6. Risks and open questions
7. Rollout / analytics

Hand to engineering with enough edge cases (payments, empty states, permissions) that design and API contracts can start.

## Mistakes to Avoid
- Specifying UI pixels without user outcome or metrics.
- No non-goals — everything looks mandatory.
- Writing PRDs after the code ships (retroactive fiction).

## Comparison
- vs tech design doc: PRD is product/outcome; TDD is how the system is built.
- vs backlog tickets: PRD sets direction; tickets schedule slices.

## Real-World Applications
Kick off a marketplace or AI feature with a PRD so design, eng, and stakeholders share the same MVP boundary.

**Example:** Stakeholder asks for five integrations in v1 — move four to non-goals and keep one path measurable.

## Pros/Cons or Trade-offs
- **Pro:** Aligns teams; reduces thrash mid-sprint.
- **Con:** Over-long PRDs rot; keep them living and short.
