[[SOLID]] [[KISS]] [[System design]] [[API design]]

# DRY

> DRY (Don't Repeat Yourself) means every piece of knowledge has one authoritative representation — duplication of *rules*, not mere similar text.

## Interview Relevance

Show you distinguish business-rule duplication from coincidental similarity, and know the rule of three / wrong-abstraction trap.

## Sources

- Hunt & Thomas, *The Pragmatic Programmer* — DRY — deep-dive
- Martin Fowler, “Duplicated Code” refactoring catalog — overview

## Key Concepts

- **Single source of truth** for invariants and policies.
- **Coincidental similarity ≠ DRY violation.**
- **Centralize:** domain module, OpenAPI/protobuf, IaC modules, runbooks.
- **Rule of three:** tolerate two copies; extract on third proven same rule.

## Technical Details

| Repeated knowledge (bad) | Coincidental similarity (often fine) |
|--------------------------|--------------------------------------|
| Tax calc in web, mobile, reports | Similar DTOs in different contexts |
| Authz rule in gateway + every service | Two unrelated `for` loops |
| Retry policy copy-pasted | Modules with no shared change driver |

```txt
Business rules → domain / shared lib (version carefully)
API contracts  → OpenAPI / protobuf ([[API design]])
Infrastructure → Terraform modules, Helm
Ops policy     → one runbook linked from alerts
```

| Principle | Tension | Resolution |
|-----------|---------|------------|
| [[KISS]] | Abstractions obscure | Extract when second change driver appears |
| [[SOLID]] | SRP splits similar code | Different actors → keep separate |
| Microservices | Shared lib couples deploys | Contract tests over fat jars |

Anti-patterns: mega-utility everyone fears; stringly-typed config drift; copy-paste microservices.

## Real-World Applications

Shared validation libraries, schema-first APIs, and Terraform modules for repeated infra.

## Pros/Cons or Trade-offs

- **Pro:** Changes land once; fewer drift bugs.
- **Con:** Wrong abstraction couples unrelated change drivers.
- **Trade-off:** shared library vs duplicated code with independent evolution.

## Comparison

- vs [[KISS]]: simplicity may prefer local duplication until proven.
- vs [[SOLID]] SRP: similar-looking code can still have different reasons to change.

## Mistakes to Avoid

- Deduplicating on appearance alone.
- Fat shared jars that force lockstep deploys.
- Documenting the same key three different names across env/Helm/docs.
