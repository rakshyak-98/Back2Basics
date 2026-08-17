[[Design pattern]] [[Design pattern/Bridge]] [[Design pattern/Decorator]]

# Adapter

> Adapter wraps an incompatible interface so existing code can call it as if it were the expected type — classic fix for third-party APIs that do not match your domain model.





## Interview Relevance
Adapter questions check whether you retrofit incompatible APIs without leaking the adaptee — contrast with Bridge (planned split) and Facade (simplify subsystem).

## Sources
- Gamma et al., *Design Patterns* (Adapter) — deep-dive

## Key Concepts
```
Class adapter:  Client → Adapter extends Target, holds Adaptee
Object adapter: Client → Adapter implements Target, delegates to Adaptee
```

Object adapter (composition) is more common — no inheritance coupling to the legacy class.

## Technical Details
Legacy `LegacyLogger.log(msg string)` vs your `Logger.info(level, msg)`:

```typescript
class LegacyLoggerAdapter implements Logger {
  constructor(private legacy: LegacyLogger) {}
  info(_level: Level, msg: string) { this.legacy.log(msg) }
}
```

## Real-World Applications
- Vendor SDK, legacy service, or OS API with wrong shape.
- Gradual migration: wrap old module, swap adapter for native implementation later.

## Comparison
**vs similar patterns**

| Pattern | Intent |
|---------|--------|
| **Adapter** | Make *existing* object fit *expected* interface |
| [[Design pattern/Bridge]] | Split abstraction from implementation upfront |
| [[Design pattern/Decorator]] | Add behavior; same interface |
| [[Design pattern/Proxy]] | Control access; same interface |

Adapter is **retrofit**; Bridge is **planned** separation.

## Mistakes to Avoid
- Leaking adaptee types through the adapter API.
- Adapter that re-implements half the adaptee — consider a full facade ([[Design pattern/Facade]]) instead.
