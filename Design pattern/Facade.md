[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]] [[Design pattern/Factory Method]] [[Architectures/Orchestration layer]]

# Facade

> One simple entry point over a noisy subsystem — keep routes/controllers dumb — **Dive Into Design Patterns + ServicesManageApi**.

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Marketing (or any) subsystem has factories, validators, pipelines, adapters. App layers should not know that graph. Facade exposes a small stable API (`launchCampaign`, `getInsights`) and wires the internals.

```
Flutter / REST controllers
        │
        ▼
  ServicesManageApi  (Facade)
        │
   ┌────┴────┬─────────┬──────────┐
Pipeline  Factory  EventBus  Commands
```

| Role | Responsibility |
|------|----------------|
| **Facade** | Coarse operations; owns orchestration entry |
| **Subsystem classes** | Real work — never called from controllers |
| **Client** | UI / REST / other BC — depends only on Facade |

## Standard config / commands

```typescript
class ServicesManageApi {
  constructor(
    private runtime: MarketingApiRuntime,
    private createFactory: (p: string) => MarketingPlatformFactory,
  ) {}

  async launchCampaign(platform: string, input: LaunchInput) {
    const factory = this.createFactory(platform);
    const cmd = new LaunchCampaignCommand(factory, this.runtime.eventBus);
    return cmd.execute(input);
  }

  async getInsights(platform: string, campaignId: string) {
    return this.createFactory(platform).createInsightsService().fetch(campaignId);
  }
}

// route — no Graph fields, no strategy switches
app.post('/launch', async (req, res) => {
  const result = await servicesManageApi.launchCampaign(req.body.platform, req.body);
  res.json(result);
});
```

### Keep contracts stable

Facade is the **compatibility layer** for Flutter/REST. Internal pattern refactors should not force client changes unless the task explicitly changes the contract.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Controllers import Graph client | Facade bypass | Move call behind Facade method |
| Facade became god class | Too many unrelated ops | Split by bounded context; keep thin |
| Every internal rename breaks mobile | Clients coupled past Facade | Version Facade DTOs |
| Duplicate orchestration in 2 Facades | Parallel entry points | One app-facing Facade per subsystem |

## Gotchas

> [!WARNING]
> Facade is not a dumping ground. If it grows validation + mapping + HTTP, you rebuilt the god service — push work into Pipeline / Strategy / Adapter.

- Facade may *use* other patterns; it should not *reimplement* them.
- Do not expose subsystem types in Facade return values if that freezes internals.

## When NOT to use

- Module already has one clear function and no subsystem — extra class is noise.
- Need to swap algorithms only — [[Design pattern/Strategy pattern]].

## Related

[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Command]] [[Design pattern/Template Method]] [[Design pattern/Factory Method]] [[Architectures/Orchestration layer]]
