[[open standard]] [[Release cycle]] [[general]]

# de facto

> De facto standard — so widely used it behaves like a standard without a formal vote.

```txt
        de facto ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shows you can separate market habit from ratified specs, and name lock-in / d…

## Sources
- [Wikipedia — De facto standard](https://en.wikipedia.org/wiki/De_facto_standard) — overview
- [IETF — Internet Standards Process (RFC 2026)](https://datatracker.ietf.org/doc/html/rfc2026) — deep-dive (de jure path)

## Key Concepts
- **De jure:** Written, reviewed, versioned by a recognized body.
- **De facto:** Git, Docker Desktop habits, “S3-compatible” APIs, common OAuth shapes
- **Interop lag:** Clients implement the popular behavior
- **Risk surface:** Vendor lock-in, silent breaking changes, and “the docs lie” when habit diverg…


- **Core:** A de facto standard wins through adoption and interoperability pressure, not …

## Technical Details
- Teams treat a de facto API as a contract when: multiple vendors clone it, SDK…
- Governance then becomes changelog discipline and compatibility tests

## Mistakes to Avoid
- **Mistake:** Equating “everyone uses it” with “it’s safe forever.”
- **Mistake:** Ignoring that de facto APIs can still require licenses or tradem…
- **Mistake:** Building only to one vendor’s quirks without an anti-corruption …

## Pros/Cons or Trade-offs
- **Pro:** Fast industry alignment; rich tooling and hiring familiarity.
- **Con:** Spec drift, sudden deprecation, and weaker recourse than a ratified open standard.

## Comparison
- vs [[open standard]]: open standards emphasize documented, implementable rule…


### Use cases
- Choosing object storage: AWS S3 API shape became de facto
