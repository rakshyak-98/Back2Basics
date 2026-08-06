[[Design pattern]] [[Design pattern/Decorator]] [[Design pattern/Facade]] [[Design pattern/Dependency Injection]]

# Proxy

> Surrogate that controls access to a real object — lazy init, auth, caching — **Dive Into Design Patterns + MetaClientProxy**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Same interface as the real subject. Proxy decides *when* and *whether* to forward. Common in API clients: delay constructing the decorated Graph client until first use; enforce token present; cache.

```
Caller → MetaClientProxy → (lazy) Decorator stack → RawMetaClient
```

| Role | Responsibility |
|------|----------------|
| **Subject** | Shared interface |
| **Real subject** | Expensive / sensitive object |
| **Proxy** | Access control, lazy create, cache |

## Standard config / commands

```typescript
class MetaClientProxy implements MetaClient {
  private real: MetaClient | null = null;

  constructor(private factory: () => MetaClient) {}

  private ensure(): MetaClient {
    if (!this.real) this.real = this.factory();
    return this.real;
  }

  request(path: string, body?: unknown) {
    return this.ensure().request(path, body);
  }
}

// composition root — factory builds Decorator stack once on first call
const client = new MetaClientProxy(() =>
  new LoggingMetaClient(new RetryMetaClient(new RawMetaClient(getToken()))),
);
```

### vs Decorator

| | Proxy | Decorator |
|--|-------|-----------|
| Intent | Control access | Add behavior |
| Typical | Lazy, security, remote, cache | Log, retry, metrics |
| Often | One proxy | Stack of decorators |

Structure is nearly identical — name by intent.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Client never initializes | Factory throws / never called | Fail on first request with clear error |
| Stale token forever | Proxy cached client at boot | Recreate on auth refresh or short TTL |
| Proxy leaks Real type | Downcast in callers | Depend on Subject interface only |

## Gotchas

> [!WARNING]
> Lazy proxy + mutable process config (Graph API version) can pin the wrong version — recreate when runtime config changes ([[Design pattern/Singleton]] runtime wiring).

## When NOT to use

- Object is cheap and always needed — construct directly.
- Only adding behavior with no access control — [[Design pattern/Decorator]].

## Related

[[Design pattern]] [[Design pattern/Decorator]] [[Design pattern/Adapter]] [[Design pattern/Singleton]] [[Design pattern/Facade]]
