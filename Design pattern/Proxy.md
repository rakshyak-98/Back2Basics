[[Design pattern]] [[Design pattern/Decorator]] [[Design pattern/Adapter]]

# Proxy

> Proxy provides a stand-in object that controls access to another — lazy loading, remote calls, permissions, or logging without changing the real subject's interface.

## Common proxy types

| Type | Behavior |
|------|----------|
| **Virtual** | Lazy-create expensive object on first use |
| **Remote** | Local representative for object on another machine (RMI, gRPC stub) |
| **Protection** | Check permissions before forwarding |
| **Logging / caching** | Intercept calls (overlaps with [[Design pattern/Decorator]]) |

```
Client → Proxy.operation()
            → (optional checks)
            → RealSubject.operation()
```

## vs Decorator

Both wrap and delegate. Proxy usually manages **lifecycle or access** of one subject; Decorator **stacks** optional behavior.

## When to use

- Large images/documents loaded on demand.
- API clients that need retries, auth injection, or metering at the boundary.

## Pitfalls

- Proxy that changes semantics silently (caching stale data).
- Remote proxy without timeout and circuit breaking — failures look like hangs.

## Sources

- Gamma et al., *Design Patterns* (Proxy)
- [Proxy pattern — Wikipedia](https://en.wikipedia.org/wiki/Proxy_pattern)
