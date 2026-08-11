[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Template Method]] [[System Design/SOLID]]

# Strategy pattern

> Strategy pattern — encapsulate what varies. When behavior branches by type (payment gateway, campaign goal, compression codec), put each variant in its own class implementing a

---

## Mental model

**Encapsulate what varies.** When behavior branches by type (payment gateway, campaign goal, compression codec), put each variant in its own class implementing a shared interface. The context holds a strategy reference and delegates — no `switch` sprayed through the codebase.

```
Context ──holds──► Strategy (interface)
                      │
           ┌──────────┼──────────┐
      GoalLeads   GoalCalls   GoalVisits
```

| Role | Responsibility |
|------|----------------|
| **Strategy** | Interface / abstract API (`buildOdaxConfig()`) |
| **Concrete strategy** | One algorithm each |
| **Context** | Business object that *uses* a strategy; may swap at runtime |
| **Registry** | Map `goalId → Strategy` — OCP extension seam |

## Standard config / commands

### TypeScript shape

```typescript
interface GoalStrategy {
  readonly id: string;
  buildConfig(input: CampaignInput): OdaxConfig;
}

class GetLeadsStrategy implements GoalStrategy {
  id = 'leads';
  buildConfig(input: CampaignInput) {
    return { optimization_goal: 'LEAD_GENERATION', /* … */ };
  }
}

const GOAL_STRATEGIES: Record<string, GoalStrategy> = {
  leads: new GetLeadsStrategy(),
  calls: new GetCallsStrategy(),
};

function resolveGoal(id: string): GoalStrategy {
  const s = GOAL_STRATEGIES[id];
  if (!s) throw new Error(`Unknown goal: ${id}`);
  return s;
}
```

### Extending (OCP)

1. Add `NewGoalStrategy` implementing the interface.
2. Register in `GOAL_STRATEGIES`.
3. Do **not** edit existing strategies or sprinkle `if (goal === 'new')`.

### Separating what changes

Pull methods that vary out of the context class into strategy classes. Context programs to the interface — never to concrete strategy types (`instanceof` is a smell).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Still editing switches in 5 files | Bypass / forgotten registry | One resolve function; ban raw switches |
| New goal needs core changes | Interface too thin or too fat | Widen strategy API or split strategies ([[System Design/SOLID]] ISP) |
| Wrong config at runtime | Bad registry key / default | Fail closed on unknown id |
| Strategies share 80% code | Copy-paste | Shared helpers module — not a mega base class |
| Tests couple to Meta fields | Strategy returns vendor DTOs | Return domain config; [[Design pattern/Adapter]] translates |

## Gotchas

> [!WARNING]
> **Inheritance for reuse** is the classic smell Strategy replaces: one superclass, override everywhere, change ripples to all subclasses.

- Runtime swap needs a setter or new context — don't mutate shared singleton strategies with request state.
- Strategy ≠ State — State transitions are internal; Strategy is chosen by the caller/configuration.
- Tiny two-branch `if` is fine; extract Strategy when a third variant or second call site appears.

## When NOT to use

- One algorithm, no planned variants.
- Variants differ only by data (configuration object / lookup table), not behavior.

## Related

[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/State]] [[Design pattern/Template Method]] [[Design pattern/Dependency Injection]] [[System Design/SOLID]]
