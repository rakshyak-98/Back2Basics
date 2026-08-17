[[Design pattern]] [[Design pattern/Decorator]] [[Design pattern/Adapter]]

# Proxy

> Proxy provides a stand-in object that controls access to another — lazy loading, remote calls, permissions, or logging without changing the real subject's interface.

```txt
        Proxy ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Proxy interviews cover access control, lazy init, and remoting

## Sources
- Gamma et al., *Design Patterns* (Proxy) — deep-dive

## Technical Details
- **Common proxy types:** 

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

## Mistakes to Avoid
- **Mistake:** Proxy that changes semantics silently (caching stale data)
- **Mistake:** Remote proxy without timeout and circuit breaking

## Comparison
- **vs Decorator**

- Both wrap and delegate. Proxy usually manages **lifecycle or access** of one …


### Use cases
- Large images/documents loaded on demand.
- API clients that need retries, auth injection, or metering at the boundary.
