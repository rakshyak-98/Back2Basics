[[de facto]] [[Release cycle]]

# open standard

> Open standard — a documented rule set anyone can implement without asking a single vendor for permission.





## Interview Relevance
Tests whether you can argue interoperability and lock-in: RFCs, W3C, ISO vs proprietary APIs that look “standard” but are not.

## Sources
- [Wikipedia — Open standard](https://en.wikipedia.org/wiki/Open_standard) — overview
- [IETF Datatracker](https://datatracker.ietf.org/) — deep-dive (example: protocol RFCs)

## Core Definition
An open standard is publicly documented, developed through a reasonably open process, and available for implementation without proprietary control that blocks independent products.

## Key Concepts
- **Documented contract:** Clear syntax/semantics and versioning (e.g. HTTP, TLS, JSON, JWT as RFCs).
- **Multiple implementations:** Competing servers/clients prove the standard is real.
- **Royalty / RAND tension:** “Open” debates often hinge on patent licensing — know the politics exist.
- **Conformance:** Test suites and profiles reduce “almost interoperable” failures.

## Technical Details
Example stack that is largely open-standard based: TCP/IP (RFCs) → TLS → HTTP → JSON. Contrast with a vendor REST that only works with one SDK and undocumented edge cases. Formal process examples: IETF Internet-Draft → RFC; W3C Recommendation.

## Real-World Applications
Choosing identity: OAuth 2.0 / OpenID Connect specs let you swap IdPs. Choosing message formats: prefer IETF/W3C media types over bespoke binary without a published schema.

## Pros/Cons or Trade-offs
- **Pro:** Portability, second-source vendors, longer lifespan than one product.
- **Con:** Slower evolution; committees; partial implementations still break you in practice.

## Comparison
vs [[de facto]]: market habit can dominate even without openness; open standards aim for implementability and governance. Related: [[Release cycle]] when standards versions force coordinated upgrades.

## Mistakes to Avoid
- Calling a single-vendor API an “open standard” because it has a PDF.
- Ignoring version negotiation and deprecated cipher suites / features.
- Assuming “open” means free of patents or compliance obligations.
