[[SOLID]] [[KISS]] [[System design]] [[API design]]

# DRY

> DRY (Don't Repeat Yourself) means every piece of knowledge should have a single, authoritative representation in the system — duplication of *logic* and *rules*, not mere similarity of text.

---

## What DRY is actually about

The Pragmatic Programmer (Hunt & Thomas) coined DRY: when the same **business rule** or **invariant** lives in three places, a change in one without the others creates defects.

| Repeated knowledge (bad) | Coincidental similarity (often fine) |
|--------------------------|--------------------------------------|
| Tax calculation in web, mobile, and report service | Two similar data transfer object shapes for different bounded contexts |
| Authorization rule in gateway and every microservice | Two `for` loops that happen to look alike |
| Retry policy copy-pasted per client | Separate modules that share no change driver |

DRY is about **coupling to a single source of truth**, not eliminating every duplicated line of code.

## Where to centralize

```txt
Business rules     → domain module / shared library (careful with versioning)
API contracts      → OpenAPI / protobuf schema ([[API design]])
Infrastructure     → Terraform modules, Helm charts
Operational policy → one runbook, linked from alerts
```

At system scale, **schema-first** application programming interfaces and **shared validation libraries** prevent drift between producer and consumer.

## DRY versus other principles

| Principle | Tension with DRY | Resolution |
|-----------|------------------|------------|
| [[KISS]] | Abstraction to deduplicate can obscure | Extract only when a second *change driver* appears |
| [[SOLID]] | Single Responsibility may split code that looks similar | Similar code serving different actors should stay separate |
| Microservices | Shared library couples deploys | Prefer contract tests over fat shared jars |

**Rule of three:** tolerate two copies; refactor on the third *proven* duplication of the same rule.

## Anti-patterns

- **Wrong abstraction** — one mega-utility that every team fears touching.
- **Stringly-typed configuration** — same key defined in environment variables, Helm, and documentation with different names.
- **Copy-paste microservices** — identical handlers in ten services instead of one library or sidecar.

*When would you duplicate instead of abstract?* When two pieces look alike today but change for different reasons tomorrow — premature DRY creates the wrong seam.

## Sources

- Andrew Hunt & David Thomas, *The Pragmatic Programmer* (Addison-Wesley, 1999) — DRY principle.
- Martin Fowler, "Duplicated Code" — refactoring catalog ([refactoring.com](https://refactoring.com/catalog/)).
