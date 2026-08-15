[[general]] [[INDEX]] [[AGENT_NOTE_RULES]] [[Release cycle]] [[Code review]]

# staff engineer

> Staff engineer — technical leadership through scope, influence, and craft — not through managing headcount.

## Interview Relevance
“Staff-plus” interviews probe impact beyond your tickets: how you unblock teams, set technical direction, reduce risk, and raise the quality bar. Value is measured by others’ throughput and system health, not personal story points.

## Sources
- [StaffEng — Staff archetypes](https://staffeng.com/guides/staff-archetypes/) — overview
- [Google SRE Book — Embracing Risk](https://sre.google/sre-book/embracing-risk/) — deep-dive (operational maturity)

## Core Definition
A staff engineer shapes the environment where problems get solved: architecture boundaries, execution paths, mentorship, and incident-ready knowledge — across teams or a deep technical domain.

## Key Concepts
- **Scope vs title:** Staff work spans multiple teams, a critical platform, or a company-wide technical bet.
- **Influence without authority:** RFCs, prototypes, [[Code review]] standards, and trusted incident leadership.
- **Tech strategy:** Choose boring technology where risk is high; invent where it creates leverage.
- **Force multiplication:** Docs, platforms, and playbooks that make mid-level engineers faster ([[general]], this vault’s mission).
- **Archetypes:** Tech lead, architect, solver, right-hand — different shapes, same impact bar.

## Technical Details
Interview map (words you can say):

| Signal | What they want | Example |
|--------|----------------|---------|
| Scope | Cross-team or company-critical blast radius | “I owned the checkout reliability SLO across three services.” |
| Judgment | Trade-offs under constraints | “We chose flags + expand/contract over a big-bang cutover.” |
| Execution | Shipped outcomes, not slide decks | “Reduced p99 by X; rollback criteria in [[Release cycle]].” |
| Mentorship | Others’ growth | “Review rubric + design office hours.” |

## Real-World Applications
Leading a payment migration: write the RFC, define rollback, coach two teams through adapters, and leave runbooks in the vault so on-call does not page you for tribal knowledge.

## Pros/Cons or Trade-offs
- **Pro:** High leverage; shapes org technical destiny.
- **Con:** Ambiguous success metrics; easy to become a bottleneck or “architecture astronaut.”

## Comparison
vs engineering manager: EM owns people and delivery process; staff owns technical outcomes and depth. vs senior IC: senior owns a service well; staff owns the *system of services* or the org’s hardest bet.

## Mistakes to Avoid
- Confusing meetings and docs with shipped risk reduction.
- Solving every problem yourself instead of enabling owners.
- Ignoring operational reality (SLOs, [[Release cycle]], on-call pain).
- Gatekeeping without teaching the path to “yes.”
