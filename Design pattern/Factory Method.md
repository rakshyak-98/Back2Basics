[[Design pattern]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Dependency Injection]] [[System Design/SOLID]]

# Factory Method

> Defer instantiation to a method subclasses (or a registry) can override — caller depends on product interface, not `new Concrete` — **Dive Into Design Patterns**.

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Trade-offs]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Creation is not the creator's main job — the creator already has business logic. Factory Method isolates *which* concrete product appears so you can add variants without editing call sites.

```
Creator.createProduct()  ──►  Product (interface)
        ▲                           ▲
 PlatformFactory              MetaServices / GoogleServices
 createPlatformFactory(id)    ← chooses family entry
```

| Role | Responsibility |
|------|----------------|
| **Product** | Interface returned to callers |
| **Concrete product** | `MetaMarketingFactory`, … |
| **Creator** | Declares `createProduct()`; uses product via interface |
| **Concrete creator** | Overrides to return a specific product |

In JS/TS services, a **registry function** (`createPlatformFactory(platformId)`) often replaces subclassing — same intent, less hierarchy.

## Core idea

…

## Variations / implementations

…

## Standard config / commands

```typescript
interface MarketingPlatformFactory {
  campaignService(): CampaignService;
  insightsService(): InsightsService;
}

function createPlatformFactory(platform: string): MarketingPlatformFactory {
  switch (platform) {
    case 'meta':
      return new MetaMarketingFactory(/* deps */);
    case 'google':
      return new GoogleMarketingFactory(/* deps */);
    default:
      throw new Error(`Unsupported platform: ${platform}`);
  }
}

// call sites never `new MetaMarketingFactory`
const factory = createPlatformFactory(req.platform);
await factory.campaignService().launch(dto);
```

### vs Abstract Factory

| | Factory Method | Abstract Factory |
|--|----------------|------------------|
| Creates | One product type | Family of related products |
| Extension | New creator / registry entry | New factory class for the family |
| Project use | `createPlatformFactory()` | `MetaMarketingFactory` methods |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Call sites still `new Concrete` | Factory bypassed | Route all construction through factory |
| Switch grows forever | Many products, one method | Split factories or use registry map |
| Can't test without Meta | Factory returns concrete only | Inject factory or product interface |
| Wrong platform in prod | Config / header mapping | Fail on unknown; log resolved id |

## Gotchas

> [!WARNING]
> Factory Method return type must be the **interface**. If the base declares `MetaClient`, subclasses cannot honestly return other vendors.

- Creator owning too much business + creation → split: keep factory thin, pipeline owns orchestration ([[Design pattern/Template Method]]).
- Static factory methods are fine; "Factory" class hierarchy is optional.

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- Single concrete type forever — `new` at composition root is clearer.
- Building one complex object with many optional fields — use [[Design pattern/Builder]].

## Related

[[Design pattern]] [[Design pattern/Creation pattern/Abstract Factory]] [[Design pattern/Builder]] [[Design pattern/Dependency Injection]] [[Design pattern/Facade]]
