[[Projects]] [[Descriptive/Javascript]]

# Project assignment (take-home)

> Time-boxed engineering exercise — ship a thin vertical slice that matches the brief’s read/write mix, not an overbuilt platform.

```txt
        Project assignment ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Hiring loops watch product sense under constraints: prioritize high-frequency…

## Sources
- [Wikipedia — Open Graph protocol](https://en.wikipedia.org/wiki/Open_Graph_protocol) — overview

## Key Concepts
- **Brief first:** objective beats preferred stack pedantry (React/Vue/etc. as allowed).
- **Read/write mix:** design caches and indexes for hot reads; validate hot writes.
- **Vertical slice:** one path works end-to-end (auth → core action → persistence).
- **Demo evidence:** screenshots/GIF + short README beats unfinished architecture diagrams.

## Technical Details
- Example classroom-style traffic shape from a brief:

| Action | Type | Rough frequency | Priority |
|--------|------|-----------------|----------|
| Create classes | write | few/day | High |
| View classes | read | ~1000/day | High |
| Comments | read/write | low | Low |
| Book class | write | few/day | Low |

- If the brief asks for dynamic Open Graph images, generate `og:image` at reque…

## Mistakes to Avoid
- **Mistake:** Building every table in the prompt instead of the high-priority …
- **Mistake:** Skipping auth on writes because “it is a demo.”
- **Mistake:** No README with run steps and assumptions

## Pros/Cons or Trade-offs
- **Pro:** Shows judgment under time limits.
- **Con:** Over-scoping signals poor prioritization.

## Comparison
- vs [[online business PRD]]: PRD defines a product; a take-home is a constrained proof.
- vs system-design review: take-home expects running code; whiteboard expects trade-offs.


### Use cases
- Treat take-homes like production triage: clarify acceptance checks, cut low-p…

- **Example:** Views dominate
