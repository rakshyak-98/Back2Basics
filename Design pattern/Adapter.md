[[Design pattern]] [[Design pattern/Bridge]] [[Design pattern/Decorator]]

# Adapter

> Adapter wraps an incompatible interface so existing code can call it as if it were the expected type — classic fix for third-party APIs that do not match your domain model.

```txt
        Adapter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Adapter questions check whether you retrofit incompatible APIs without leakin…

## Sources
- Gamma et al., *Design Patterns* (Adapter) — deep-dive

## Key Concepts
```
- **Note:** Class adapter: Client → Adapter extends Target, holds Adaptee
- **Note:** Object adapter: Client → Adapter implements Target, delegates to Adaptee
```

- **Note:** Object adapter (composition) is more common

## Technical Details
- Legacy `LegacyLogger.log(msg string)` vs your `Logger.info(level, msg)`:

```typescript
class LegacyLoggerAdapter implements Logger {
  constructor(private legacy: LegacyLogger) {}
  info(_level: Level, msg: string) { this.legacy.log(msg) }
}
```

## Mistakes to Avoid
- **Mistake:** Leaking adaptee types through the adapter API
- **Mistake:** Adapter that re-implements half the adaptee

## Comparison
- **vs similar patterns**

| Pattern | Intent |
|---------|--------|
| **Adapter** | Make *existing* object fit *expected* interface |
| [[Design pattern/Bridge]] | Split abstraction from implementation upfront |
| [[Design pattern/Decorator]] | Add behavior; same interface |
| [[Design pattern/Proxy]] | Control access; same interface |

- Adapter is **retrofit**; Bridge is **planned** separation.


### Use cases
- Vendor SDK, legacy service, or OS API with wrong shape.
- Gradual migration: wrap old module, swap adapter for native implementation later.
