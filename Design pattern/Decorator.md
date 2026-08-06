[[Design pattern]] [[Design pattern/Proxy]] [[Design pattern/Adapter]] [[Design pattern/Dependency Injection]]

# Decorator

> Wrap an object to add behavior without changing its interface — stack concerns — **Dive Into Design Patterns + logging/retry around Graph client**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Instead of subclassing `MetaClient` into `LoggingMetaClient`, `RetryMetaClient`, `LoggingRetryMetaClient`, … wrap the same interface:

```
MetaClient
  └─ RetryDecorator
       └─ LoggingDecorator
            └─ RawMetaClient
```

Callers still see `MetaClient`. Order of wrapping matters (retry outside logging vs inside).

| Role | Responsibility |
|------|----------------|
| **Component** | Interface (`request(path, body)`) |
| **Concrete component** | Real HTTP client |
| **Decorator** | Implements interface; holds inner component; adds work before/after |

## Standard config / commands

```typescript
interface MetaClient {
  request(path: string, body?: unknown): Promise<unknown>;
}

class LoggingMetaClient implements MetaClient {
  constructor(private inner: MetaClient) {}
  async request(path: string, body?: unknown) {
    console.log('graph', path);
    try {
      const res = await this.inner.request(path, body);
      console.log('graph ok', path);
      return res;
    } catch (e) {
      console.error('graph fail', path, e);
      throw e;
    }
  }
}

class RetryMetaClient implements MetaClient {
  constructor(private inner: MetaClient, private times = 3) {}
  async request(path: string, body?: unknown) {
    let last: unknown;
    for (let i = 0; i < this.times; i++) {
      try {
        return await this.inner.request(path, body);
      } catch (e) {
        last = e;
      }
    }
    throw last;
  }
}

const client: MetaClient = new LoggingMetaClient(
  new RetryMetaClient(new RawMetaClient(token)),
);
```

### Composition over inheritance

Favor decorator stacks for cross-cutting concerns. Subclassing for every combination is the anti-pattern the book (and production Graph clients) warn against.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Double logging / double retry | Wrapped twice | Compose once at composition root |
| Retry hides 4xx forever | Retrying non-idempotent / client errors | Retry only 429/5xx; respect Retry-After |
| Decorator breaks interface | Extra methods only on wrapper | Keep strict same interface |
| Hard to test order | Opaque stack | Unit-test each decorator with fake inner |

## Gotchas

> [!WARNING]
> Decorator that changes return semantics (swallows errors, mutates payload) surprises callers — keep additive and transparent.

- Proxy vs Decorator — Proxy controls *access* (lazy, auth, caching); Decorator *adds* behavior. Same structure, different intent. See [[Design pattern/Proxy]].
- Do not put domain mapping in Decorator — [[Design pattern/Adapter]].

## When NOT to use

- Single concern, single class — plain wrapper function is enough.
- Need to change the interface — Adapter, not Decorator.

## Related

[[Design pattern]] [[Design pattern/Proxy]] [[Design pattern/Adapter]] [[Design pattern/Bridge]] [[Design pattern/Dependency Injection]]
