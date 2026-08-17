[[staff engineer]] [[general]] [[INDEX]] [[AGENT_NOTE_RULES]] [[README]]

# we

> We — this vault’s mission: force-multiply engineers with field notes you can retrieve, debug, and configure under incident pressure.

```txt
        we ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Culture questions (“how do you share knowledge?”) map here: durable notes bea…

## Sources
- Vault: [[AGENT_NOTE_RULES]] — deep-dive
- Vault: [[staff engineer]] — overview
- [Google SRE — Knowledge sharing themes](https://sre.google/sre-book/table-of-contents/) — overview

## Key Concepts
- **Force multiplication:** One clear note saves N future engineers N minutes each.
- **Pressure-ready:** Prefer checks, commands, and failure modes over essay history.
- **Networked knowledge:** Wikilinks and hubs ([[INDEX]], [[general]]) over isolated dumps.
- **Craft bar:** Mind Map or Cornell shape for leaf topics ([[AGENT_NOTE_RULES]]).


- **Core:** **we** marks the intent of Back2Basics: operational field notes for a team

## Technical Details
| Need | Open |
|------|------|
| Symptom under pressure | [[INDEX]] |
| How notes are written | [[AGENT_NOTE_RULES]] |
| Domain navigation | [[general]] |
| Staff-level expectations | [[staff engineer]] |
| Vault overview | [[README]] |

- Mission loop: incident → note gap found → write/fix leaf → next on-call is fa…

## Mistakes to Avoid
- **Mistake:** Writing notes nobody can find from [[INDEX]]
- **Mistake:** Empty placeholder sections that look complete
- **Mistake:** Capturing secrets or customer data in the vault

## Pros/Cons or Trade-offs
- **Pro:** Compounds team speed; onboarding shortcut; study prep as a byproduct.
- **Con:** Notes rot without owners; vanity pages without links help no one.

## Comparison
- vs personal scratchpad: this is team-facing and linked


### Use cases
- After a DRM or Kafka outage, capture the repro, the metric that fired, and th…
