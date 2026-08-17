[[de facto]] [[Release cycle]]

# open standard

> Open standard — a documented rule set anyone can implement without asking a single vendor for permission.

```txt
        open standard ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Tests whether you can argue interoperability and lock-in: RFCs, W3C, ISO vs p…

## Sources
- [Wikipedia — Open standard](https://en.wikipedia.org/wiki/Open_standard) — overview
- [IETF Datatracker](https://datatracker.ietf.org/) — deep-dive (example: protocol RFCs)

## Key Concepts
- **Documented contract:** Clear syntax/semantics and versioning (e.g. HTTP, TLS, JSON, JWT as RFCs).
- **Multiple implementations:** Competing servers/clients prove the standard is real.
- **Royalty / RAND tension:** “Open” debates often hinge on patent licensing — know the politics exist.
- **Conformance:** Test suites and profiles reduce “almost interoperable” failures.


- **Core:** An open standard is publicly documented, developed through a reasonably open …

## Technical Details
- Example stack that is largely open-standard based: TCP/IP (RFCs) → TLS → HTTP…
- Contrast with a vendor REST that only works with one SDK and undocumented edg…
- Formal process examples: IETF Internet-Draft → RFC; W3C Recommendation.

## Mistakes to Avoid
- **Mistake:** Calling a single-vendor API an “open standard” because it has a …
- **Mistake:** Ignoring version negotiation and deprecated cipher suites / feat…
- **Mistake:** Assuming “open” means free of patents or compliance obligations

## Pros/Cons or Trade-offs
- **Pro:** Portability, second-source vendors, longer lifespan than one product.
- **Con:** Slower evolution; committees; partial implementations still break you in practice.

## Comparison
- vs [[de facto]]: market habit can dominate even without openness


### Use cases
- Choosing identity: OAuth 2.0 / OpenID Connect specs let you swap IdPs
