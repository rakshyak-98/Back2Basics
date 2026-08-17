[[staff engineer]] [[general]] [[INDEX]] [[AGENT_NOTE_RULES]] [[README]]

# we

> We — this vault’s mission: force-multiply engineers with field notes you can retrieve, debug, and configure under incident pressure.

## Interview Relevance
Culture questions (“how do you share knowledge?”) map here: durable notes beat tribal Slack. Staff signal: you build systems that make others faster ([[staff engineer]]).

## Sources
- Vault: [[AGENT_NOTE_RULES]] — deep-dive
- Vault: [[staff engineer]] — overview
- [Google SRE — Knowledge sharing themes](https://sre.google/sre-book/table-of-contents/) — overview

## Core Definition
**we** marks the intent of Back2Basics: operational field notes for a team — retrieve fast, debug fast, configure correctly — without hunting tutorials or raw man pages mid-incident.

## Key Concepts
- **Force multiplication:** One clear note saves N future engineers N minutes each.
- **Pressure-ready:** Prefer checks, commands, and failure modes over essay history.
- **Networked knowledge:** Wikilinks and hubs ([[INDEX]], [[general]]) over isolated dumps.
- **Craft bar:** Mind Map or Cornell shape for leaf topics ([[AGENT_NOTE_RULES]]).

## Technical Details
| Need | Open |
|------|------|
| Symptom under pressure | [[INDEX]] |
| How notes are written | [[AGENT_NOTE_RULES]] |
| Domain navigation | [[general]] |
| Staff-level expectations | [[staff engineer]] |
| Vault overview | [[README]] |

Mission loop: incident → note gap found → write/fix leaf → next on-call is faster.

## Real-World Applications
After a DRM or Kafka outage, capture the repro, the metric that fired, and the fix command in a leaf note the same week — not a month later when memory faded.

## Pros/Cons or Trade-offs
- **Pro:** Compounds team speed; onboarding shortcut; interview prep as a byproduct.
- **Con:** Notes rot without owners; vanity pages without links help no one.

## Comparison
vs personal scratchpad: this is team-facing and linked. vs official vendor docs: we add *your* failure modes and house standards. Sibling: [[general]] (navigation), [[we]] (why we bother).

## Mistakes to Avoid
- Writing notes nobody can find from [[INDEX]].
- Empty placeholder sections that look complete.
- Capturing secrets or customer data in the vault.
