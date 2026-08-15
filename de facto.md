[[open standard]] [[Release cycle]] [[general]]

# de facto

> De facto standard — so widely used it behaves like a standard without a formal vote.

## Interview Relevance
Shows you can separate market habit from ratified specs, and name lock-in / drift risks when teams “just use what everyone uses.”

## Sources
- [Wikipedia — De facto standard](https://en.wikipedia.org/wiki/De_facto_standard) — overview
- [IETF — Internet Standards Process (RFC 2026)](https://datatracker.ietf.org/doc/html/rfc2026) — deep-dive (de jure path)

## Core Definition
A de facto standard wins through adoption and interoperability pressure, not because a standards body ratified it first. De jure standards are formal (ISO, RFC, ECMA).

## Key Concepts
- **De jure:** Written, reviewed, versioned by a recognized body.
- **De facto:** Git, Docker Desktop habits, “S3-compatible” APIs, common OAuth shapes — practice leads, paper follows (or never does).
- **Interop lag:** Clients implement the popular behavior; formal specs catch up later (or fragment).
- **Risk surface:** Vendor lock-in, silent breaking changes, and “the docs lie” when habit diverges from any written rule.

## Technical Details
Teams treat a de facto API as a contract when: multiple vendors clone it, SDKs assume it, and switching cost is high. Governance then becomes changelog discipline and compatibility tests — not waiting for an RFC number.

## Real-World Applications
Choosing object storage: AWS S3 API shape became de facto; “S3-compatible” vendors compete on that habit. Choosing containers: Docker CLI UX became the mental model even when the runtime underneath is containerd/CRI-O.

## Pros/Cons or Trade-offs
- **Pro:** Fast industry alignment; rich tooling and hiring familiarity.
- **Con:** Spec drift, sudden deprecation, and weaker recourse than a ratified open standard.

## Comparison
vs [[open standard]]: open standards emphasize documented, implementable rules without proprietary lock-in; de facto may be closed or semi-documented but universally expected. Related: [[Release cycle]] when de facto tooling changes break your train.

## Mistakes to Avoid
- Equating “everyone uses it” with “it’s safe forever.”
- Ignoring that de facto APIs can still require licenses or trademark restrictions.
- Building only to one vendor’s quirks without an anti-corruption layer.
