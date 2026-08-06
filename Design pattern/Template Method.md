[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Factory Method]] [[Design pattern/Chain of Responsibility]] [[Architectures/Orchestration layer]]

# Template Method

> Fixed algorithm skeleton in a base class (or function); subclasses override steps — **Dive Into Design Patterns + LaunchPipeline**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Launch always: validate → create campaign → create adset → create creative → create ad → publish events. Platforms differ in *how* each step talks to the vendor. Template Method locks the order; overrides supply platform-specific steps.

```
LaunchPipeline.run()
  validate()        ← may use Chain
  createCampaign()  ← override per platform
  createAdSet()
  createCreative()
  createAd()
  emitEvents()      ← Observer
```

| Role | Responsibility |
|------|----------------|
| **Abstract class / base pipeline** | `run()` calls steps in order |
| **Hooks / abstract steps** | Overridden by Meta / Google pipelines |
| **Concrete class** | Platform-specific implementations |

## Standard config / commands

```typescript
abstract class LaunchPipeline {
  constructor(protected factory: MarketingPlatformFactory) {}

  async run(input: LaunchRequest): Promise<LaunchResult> {
    await this.validate(input);
    const campaign = await this.createCampaign(input);
    const adset = await this.createAdSet(input, campaign.id);
    const creative = await this.createCreative(input);
    const ad = await this.createAd(input, adset.id, creative.id);
    await this.afterLaunch({ campaign, adset, creative, ad });
    return { campaignId: campaign.id, adId: ad.id };
  }

  protected abstract validate(input: LaunchRequest): Promise<void>;
  protected abstract createCampaign(input: LaunchRequest): Promise<{ id: string }>;
  protected abstract createAdSet(input: LaunchRequest, campaignId: string): Promise<{ id: string }>;
  protected abstract createCreative(input: LaunchRequest): Promise<{ id: string }>;
  protected abstract createAd(
    input: LaunchRequest,
    adsetId: string,
    creativeId: string,
  ): Promise<{ id: string }>;

  protected async afterLaunch(_result: unknown): Promise<void> {
    /* optional hook */
  }
}

class MetaLaunchPipeline extends LaunchPipeline {
  protected async validate(input: LaunchRequest) {
    await metaValidationChain(input);
  }
  protected async createCampaign(input: LaunchRequest) {
    return this.factory.createCampaignService().create(input);
  }
  // …
}
```

### vs Strategy

| | Template Method | Strategy |
|--|-----------------|----------|
| Structure | Inheritance; shared skeleton | Composition; swap whole algorithm |
| Variation | Individual steps | Entire behavior object |
| Prefer | Stable multi-step workflow | Pluggable algorithms |

Favor composition when steps themselves are strategies — hybrid is common (pipeline + goal strategy).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Copy-paste launch flows per platform | No shared skeleton | Extract Template Method base |
| Base knows Meta fields | Leakage | Steps use factory + adapter only |
| Optional step forced | Abstract when optional | Default empty hook (`afterLaunch`) |
| Hard to test mid-step | Monolith `run` | Test concrete step overrides with fake factory |

## Gotchas

> [!WARNING]
> Deep Template Method hierarchies reintroduce the inheritance pain Strategy was meant to avoid — keep one base + one level of concretes.

- Do not put side-effects that must not fail the launch into required steps — use Observer after success.
- God pipeline that also validates, maps, and retries — split: Chain + Adapter + Decorator.

## When NOT to use

- Steps are identical — one function, no inheritance.
- Only one step varies — [[Design pattern/Strategy pattern]] or a callback hook.

## Related

[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Chain of Responsibility]] [[Design pattern/Observer]] [[Design pattern/Factory Method]] [[Architectures/Orchestration layer]]
