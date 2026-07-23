[[KISS]] [[SOLID]] [[System design]] [[Design pattern]]

# DRY (Don't Repeat Yourself)

> Single source of truth for knowledge — **dedupe logic and config**, not every similar-looking line.

---

## Mental model

**DRY** means every piece of **knowledge** (business rule, schema, validation) should have **one authoritative representation**. Change the rule once — it propagates everywhere. Confusing DRY with **"never duplicate code"** leads to premature abstractions that couple unrelated features.

```txt
Violating DRY:
  tax_rate in API, mobile app, invoice PDF, admin UI — four sources drift

Healthy DRY:
  tax_rate in config/DB → API exposes → clients consume
```

| Repeat type | DRY response | Anti-pattern |
|-------------|--------------|--------------|
| **Business rule** | Shared module / service | Copy-paste in 5 repos |
| **Schema** | OpenAPI / protobuf single gen | Hand-written DTOs |
| **Config** | Env + IaC variables | Hardcode in each service |
| **Similar UI layout** | Component library | 200-line "helper" for 2 callers |

**Divide system into pieces** with clear boundaries — reuse **across** boundaries via contracts, not `#include` everything ([[KISS]]).

---

## Standard config / commands

### DRY hierarchy (prefer top)

```txt
1. Data / config (one DB column, one tfvars)
2. Generated code (OpenAPI client, protobuf)
3. Shared library (versioned npm/maven crate)
4. Copy with comment linking canonical source (last resort)
```

### OpenAPI → clients (API single source)

```yaml
# openapi.yaml — generate TS + Go clients in CI
paths:
  /v1/orders:
    post:
      requestBody: { $ref: '#/components/schemas/CreateOrder' }
```

### Terraform variables (infra DRY)

```hcl
locals {
  common_tags = { Env = var.environment, Team = "platform" }
}
# Reuse local.common_tags — don't repeat tag maps per resource
```

See [[Terraform setup]].

### When duplication is OK (WET on purpose)

```txt
Two services same validation today — merge when rule changes twice
Test fixtures — clarity beats shared mega-fixture
Microservice independence — small duplication < shared DB coupling
```

### Refactor trigger

```txt
Rule changed in one place but not others → DRY violation confirmed → extract
Not: "these 3 lines look similar" on first sight
```

### Code review checklist

```txt
□ Does this duplicate a business rule elsewhere?
□ Is the abstraction simpler than duplication?
□ Will teams deploy independently if shared lib changes?
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Inconsistent behavior UI vs API | Forked validation | Extract shared validator; API owns truth |
| Bug fixed in one service only | Copy-paste logic | Search repo; centralize |
| Shared lib breaks all services | Tight coupling | Version lib semver; avoid breaking changes |
| "God module" imports | Over-DRY | Split by domain boundary |
| Config drift prod/stage | Duplicate env files | Single template + env overlay |
| Generated code edited by hand | Regen overwrite | Fix generator source |

---

## Gotchas

> [!WARNING]
> **DRY across microservices via shared DB** — worse than duplicated code; couples deploy.

> [!WARNING]
> **Inheritance tower for 2 subclasses** — prefer composition; DRY ≠ OOP hierarchy.

> [!WARNING]
> **DRY in tests** — opaque shared setup hides failure cause.

> [!WARNING]
> **Premature generic `executeAction(type)`** — [[KISS]] beats clever DRY.

> [!WARNING]
> **Long methods "because DRY"** — split readable methods; extract only real duplication.

---

## When NOT to use

- **Exploratory prototype** — duplication acceptable until pattern stabilizes.
- **Cross-team library for one constant** — copy or config service.
- **Identical syntax, different domain meaning** — forcing merge creates wrong coupling.

---

## Related

[[KISS]] [[SOLID]] [[System design]] [[API design]] [[marshalling]] [[Design pattern]]
