[[stateless offset handling]]

# stateless

> stateless — server that streams data to clients without storing any session/state between requests or clients.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

### Stateless streaming server
- Server that streams data to clients without storing any session/state between requests or clients.
> [!INFO] Resilient to restarts
> [!INFO] Characteristics
> - no memory of past events or client identity.
> - pure output generator per request.
> - clients responsible for tracking progress (e.g., with `Last-Event-ID`).
> - client provide context (cursor, token, offset) with each request.
> - Ideal for horizontal scaling, fault tolerance.
> - all server behavior is reproducible
- use query params or headers form cursor/offset.
- read from source (DB, Queue, etc.)
- stream to client.
- Avoid in-memory client tracking.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
