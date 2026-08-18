[[Design pattern]] [[Design pattern/Observer]] [[Design pattern/State]] [[React/React design patterns]]

# Mediator

> Mediator — creativeStep ──► CampaignWizardMediator ──► updates peers

## Mental model

Wizard steps (goal → creative → budget → review) must enable/disable each other. Without Mediator, every step imports every other step. Mediator owns the collaboration graph; colleagues talk only to the mediator.

```
GoalStep ──┐
CreativeStep ──► CampaignWizardMediator ──► updates peers
BudgetStep ──┘
```

## Standard config / commands

```typescript
class CampaignWizardMediator {
  constructor(
    private goal: GoalStep,
    private creative: CreativeStep,
    private budget: BudgetStep,
  ) {
    goal.onChange = () => this.onGoalChanged();
  }

  onGoalChanged() {
    this.creative.setAllowedTypes(this.goal.allowedCreatives());
    this.budget.setMin(this.goal.minBudget());
  }
}
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Steps import each other | Mediator bypassed | Route all cross-talk through mediator |
| Mediator god object | Too many domains | One mediator per UI flow / BC |
| State illegal for status | Lifecycle mixed in | Keep legality in [[Design pattern/State]] |

## Gotchas

> [!WARNING]
> …

## When NOT to use

- Two components — direct callback is fine.
- Global application event bus for everything — prefer [[Design pattern/Observer]] with clear event names, not one mega-mediator.

## Related

[[Design pattern]] [[Design pattern/Observer]] [[Design pattern/State]] [[React/React design patterns]]
