[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Facade]] [[System Design/KISS]]

# Builder

> Construct a complex object step by step — same construction process, different representations — **Dive Into Design Patterns + wizard → launch request**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

When an object needs many optional fields, nested parts, or ordered assembly (wizard screens → launch DTO), a Builder accumulates pieces then `build()` validates and returns the product. Director/pipeline can replay the same steps for different builders.

```
Wizard fields
  → LaunchCampaignBuilder
      .withGoal()
      .withBudget()
      .withCreative()
      .withGeo()
      .build()  → LaunchRequest
```

| Role | Responsibility |
|------|----------------|
| **Builder** | Step methods + `build()` |
| **Concrete builder** | Knows product shape |
| **Product** | Immutable launch request / domain object |
| **Director** (optional) | Fixed sequence of steps |

## Standard config / commands

```typescript
class LaunchCampaignBuilder {
  private draft: Partial<LaunchRequest> = {};

  withGoal(goalId: string) {
    this.draft.goalId = goalId;
    return this;
  }
  withBudget(daily: number, currency: string) {
    this.draft.budget = { daily, currency };
    return this;
  }
  withCreative(creative: CreativeInput) {
    this.draft.creative = creative;
    return this;
  }
  build(): LaunchRequest {
    if (!this.draft.goalId || !this.draft.budget) {
      throw new Error('LaunchRequest incomplete');
    }
    return this.draft as LaunchRequest;
  }
}

const req = new LaunchCampaignBuilder()
  .withGoal(body.goal)
  .withBudget(body.daily, body.currency)
  .withCreative(body.creative)
  .build();
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Invalid objects escape | `build()` too permissive | Validate required fields in `build()` |
| Builder reused across requests | Mutable leftover state | New builder per request or `reset()` |
| 12-arg constructor still exists | Call sites bypass builder | Delete public constructor; factory/builder only |
| Steps order-dependent bugs | Implicit ordering | Document order or enforce in Director |

## Gotchas

> [!WARNING]
> Telescoping constructors (`new X(a)`, `new X(a,b)`, …) are the smell Builder replaces — don't keep both.

- Fluent `return this` is convenience, not required.
- Builder holding a live DB connection mid-build = wrong boundary; build a DTO, then execute Command/Pipeline.

## When NOT to use

- 2–3 required fields, no optionals — constructor is clearer ([[System Design/KISS]]).
- Need a family of products — [[Design pattern/Creation pattern/Abstract Factory]].

## Related

[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Command]] [[Design pattern/Template Method]] [[Design pattern/Facade]]
