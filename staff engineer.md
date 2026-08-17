[[general]] [[INDEX]] [[Release cycle]] [[Code review]]

# staff engineer

> Staff engineer — technical leadership through scope, influence, and craft — not through managing headcount.

```txt
        staff engineer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** “Staff-plus” reviews probe impact beyond your tickets: how you unblock tea…

## Sources
- [StaffEng — Staff archetypes](https://staffeng.com/guides/staff-archetypes/) — overview
- [Google SRE Book — Embracing Risk](https://sre.google/sre-book/embracing-risk/) — deep-dive (operational maturity)

## Key Concepts
- **Scope vs title:** Staff work spans multiple teams, a critical platform, or a company-wide techn…
- **Influence without authority:** RFCs, prototypes, [[Code review]] standards, and trusted incident leadership.
- **Tech strategy:** Choose boring technology where risk is high; invent where it creates leverage.
- **Force multiplication:** Docs, platforms, and playbooks that make mid-level engineers faster ([[genera…
- **Archetypes:** Tech lead, architect, solver, right-hand — different shapes, same impact bar.


- **Core:** A staff engineer shapes the environment where problems get solved: architectu…

## Technical Details
- Review map (words you can say):

| Signal | What they want | Example |
|--------|----------------|---------|
| Scope | Cross-team or company-critical blast radius | “I owned the checkout reliability SLO across three services.” |
| Judgment | Trade-offs under constraints | “We chose flags + expand/contract over a big-bang cutover.” |
| Execution | Shipped outcomes, not slide decks | “Reduced p99 by X; rollback criteria in [[Release cycle]].” |
| Mentorship | Others’ growth | “Review rubric + design office hours.” |

## Mistakes to Avoid
- **Mistake:** Confusing meetings and docs with shipped risk reduction
- **Mistake:** Solving every problem yourself instead of enabling owners
- **Mistake:** Ignoring operational reality (SLOs, [[Release cycle]], on-call p…
- **Mistake:** Gatekeeping without teaching the path to “yes.”

## Pros/Cons or Trade-offs
- **Pro:** High leverage; shapes org technical destiny.
- **Con:** Ambiguous success metrics; easy to become a bottleneck or “architecture astronaut.”

## Comparison
- vs engineering manager: EM owns people and delivery process


### Use cases
- Leading a payment migration: write the RFC, define rollback, coach two teams …
