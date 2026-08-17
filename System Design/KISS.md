[[DRY]] [[SOLID]] [[System design]] [[API design]]

# KISS

> KISS (Keep It Simple, Stupid) urges designs that solve the present problem with the fewest moving parts that still meet requirements — complexity is a loan with interest.

```txt
        KISS ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Defend the simplest design that meets requirements

## Sources
- Kelly Johnson / Lockheed Skunk Works — KISS origin in engineering culture — overview
- Google SRE Book — "Simplicity" as operability virtue; prefer boring technology — deep-dive
- Rich Hickey, "Simple Made Easy" (Strange Loop 2011) — simplicity versus ease distinction — overview

## Key Concepts
- **Simplest design that works:** meet requirements without speculative generality.
- **Complexity budget:** every abstraction must earn its keep.
- **Revisit later:** extract when a second real change driver appears.
- **Operability counts:** simple to run beats clever on-call nights.


### Questions before adding a part

1. What requirement fails if we omit this?
- **Note:** 2. What is the operational cost (on-call, dashboards, upgrades)?
- **Note:** 3. Can we meet the service level objective with a boring solution for twelve …
- **Note:** 4. Does the team have production experience with this technology?

- **Note:** If answers are weak, defer

## Technical Details
### What simplicity means here

- Simplicity is not ignorance of scale.
- It is **refusing complexity that does not buy measurable reliability, perform…

| Simple (for now) | Complex (justify before building) |
|------------------|-----------------------------------|
| Monolith + PostgreSQL | Ten microservices day one |
| Cursor pagination | Custom search engine for 500 rows |
| Synchronous request-response | Event sourcing for a CRUD admin form |
| Managed Redis cache | Self-sharded in-memory grid |

- The United States Navy reportedly coined KISS in the 1960s for aircraft engin…

### KISS at boundaries

- [[API design]] should expose **stable product concepts**, not internal shard …
- Users and partner integrations benefit from simple mental models even when th…

### When simplicity becomes negligence

- KISS is not an excuse to skip:

- Authentication and authorization ([[Authentication web application]])
- Backups and restore drills
- Timeouts and idempotency on external calls
- Basic observability (latency, errors, saturation)

- *Boring plus reliable* beats *clever plus fragile*.

## Mistakes to Avoid
- **Mistake:** Skipping failure modes until production
- **Mistake:** Ignoring idempotency, timeouts, or rollback where required
- **Mistake:** Optimizing or distributing before measuring the real bottleneck

## Pros/Cons or Trade-offs
Extract abstractions when duplication proves the same rule changes together — not when two snippets merely look similar. Apply [[SOLID]] at real boundaries (payment gateway, storage port), not as interface-per-class theater.

*What breaks first when you over-engineer?* Team velocity — nobody dares change the framework you did not need.


- **Pro:** Faster delivery; fewer failure modes.
- **Con:** Under-design that paints into a corner.
- **Trade-off:** KISS now vs intentional extensibility for known futures.

## Comparison
- vs [[DRY]]: do not abstract solely to dedupe lookalike code.
- vs [[SOLID]]: principles serve clarity — not maximal type graphs.


### Use cases
- Early product MVPs, incident remediations, and design reviews that prune gold…
