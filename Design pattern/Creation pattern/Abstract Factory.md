[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Bridge]] [[System Design/SOLID]]

# Abstract Factory

> Create families of related products without binding to concrete classes — **Dive Into Design Patterns** (Marketing platform = campaign + adset + creative + ad + insights).

---

## Mental model

When products must match as a **set** (Meta campaign service with Meta adset service — never mix Meta + Google mid-pipeline), declare one factory interface with a create method per product. Each platform gets one concrete factory that returns the whole consistent family.

```
AbstractFactory
  createCampaign() createAdSet() createCreative() createAd() createInsights()
        │
  MetaMarketingFactory          GoogleMarketingFactory
  (all Meta-flavored)           (all Google-flavored)
```

| Role | Responsibility |
|------|----------------|
| **Abstract products** | Interfaces per product type |
| **Concrete products** | Platform-specific implementations |
| **Abstract Factory** | Interface of create* methods |
| **Concrete Factory** | One class per platform/variant |

## Standard config / commands

```typescript
interface MarketingPlatformFactory {
  createCampaignService(): CampaignService;
  createAdSetService(): AdSetService;
  createCreativeService(): CreativeService;
  createInsightsService(): InsightsService;
}

class MetaMarketingFactory implements MarketingPlatformFactory {
  constructor(private client: MetaClient) {}
  createCampaignService() { return new MetaCampaignService(this.client); }
  createAdSetService() { return new MetaAdSetService(this.client); }
  createCreativeService() { return new MetaCreativeService(this.client); }
  createInsightsService() { return new MetaInsightsService(this.client); }
}

// chosen once via Factory Method
const platform = createPlatformFactory('meta');
const pipeline = new MetaLaunchPipeline(platform);
```

### Extending (OCP)

New platform → new `*MarketingFactory` + register in [[Design pattern/Factory Method]]. Existing Meta factory and call sites stay closed.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mixed Meta/Google objects | Factory bypassed mid-flow | Hold factory on pipeline; never pick services ad hoc |
| Adding product means editing all factories | Abstract factory incomplete | Add create* to interface + all concretes |
| Fat factory knows Graph field names | Responsibilities leaked | Products own mapping; factory only wires |
| Hard to test | Real Graph client inside factory | Inject client / use [[Design pattern/Dependency Injection]] |

## Gotchas

> [!WARNING]
> Abstract Factory freezes the **product set**. Adding a product type forces interface + every concrete factory to change — accept that cost or split factories by subdomain.

- Do not confuse with Builder (one complex object) or Factory Method (one product).
- "Family" must be real — unrelated create methods in one factory is a god factory.

## When NOT to use

- Only one platform and no second planned — concrete services at composition root.
- Products are independent and never used as a matched set — separate factories / DI bindings.

## Related

[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Builder]] [[Design pattern/Bridge]] [[Design pattern/Facade]]

→ Stub typo alias: [[Design pattern/Creation pattern/Abstract Factor]]
