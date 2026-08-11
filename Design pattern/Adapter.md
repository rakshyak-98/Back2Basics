[[Design pattern]] [[Design pattern/Bridge]] [[Design pattern/Facade]] [[Design pattern/Dependency Injection]]

# Adapter

> Convert one interface into another the client expects — retrofit vendor shapes into domain — **Dive Into Design Patterns + MetaPayloadAdapter**.

---

## Mental model

Your domain speaks `LaunchRequest` / `Campaign`. Meta Graph speaks nested snake_case fields that change with API version. Adapter sits on the boundary and translates both directions so domain and controllers never touch vendor field names.

```
Domain model  ←── Adapter ──→  Vendor DTO / Graph payload
```

| Role | Responsibility |
|------|----------------|
| **Target** | Interface your app wants |
| **Adaptee** | Existing vendor client / payload shape |
| **Adapter** | Implements Target; delegates to Adaptee after mapping |

## Standard config / commands

```typescript
interface CampaignPayload {
  name: string;
  objective: string;
  specialAdCategories: string[];
}

class MetaPayloadAdapter {
  toGraph(domain: CampaignPayload): Record<string, unknown> {
    return {
      name: domain.name,
      objective: domain.objective,
      special_ad_categories: domain.specialAdCategories,
    };
  }

  fromGraph(raw: Record<string, unknown>): CampaignPayload {
    return {
      name: String(raw.name ?? ''),
      objective: String(raw.objective ?? ''),
      specialAdCategories: (raw.special_ad_categories as string[]) ?? [],
    };
  }
}
```

### vs Bridge / Facade / Decorator

| Pattern | Intent |
|---------|--------|
| **Adapter** | Make incompatible interfaces work — often retrofit |
| **Bridge** | Designed split of abstraction vs implementation upfront |
| **Facade** | Simplify a whole subsystem API |
| **Decorator** | Add behavior; same interface |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Controllers set `special_ad_categories` | Adapter skipped | Only Adapter emits Graph keys |
| Graph version change breaks app | Mapping scattered | Centralize in Adapter; version behind it |
| Silent wrong fields | Typo in map | Contract tests on Adapter fixtures |
| Fat Adapter knows launch rules | Scope creep | Mapping only; rules in Strategy/Chain |

## Gotchas

> [!WARNING]
> An "interface" that is a 1:1 mirror of Meta fields is not insulating you — the Adapter (or anti-corruption layer) must own the translation to *your* model.

- Two-way mapping drifts — prefer golden fixtures from real Graph responses.
- Do not put HTTP retry/logging in Adapter — that is [[Design pattern/Decorator]].

## When NOT to use

- You control both interfaces and can change them to match.
- Need parallel hierarchies designed to evolve — [[Design pattern/Bridge]].

## Related

[[Design pattern]] [[Design pattern/Bridge]] [[Design pattern/Facade]] [[Design pattern/Decorator]] [[Descriptive/DAP (Debug Adapter Protocol)]]
