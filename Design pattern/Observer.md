<!-- note-strategy: concept -->
[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Template Method]] [[Messaging/Web hooks]]

# Observer

> Subscribers react to events without the subject knowing who they are — **Dive Into Design Patterns + launchEventBus**.

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

After a successful launch you want metrics, audit log, webhook, cache invalidate. Subject (`LaunchEventBus`) emits; observers subscribe. Adding a side-effect = new subscription — subject stays closed (OCP).

```
LaunchPipeline ──emit──► LaunchEventBus
                            │
              ┌─────────────┼─────────────┐
           Metrics       Audit         Webhook
```

| Role | Responsibility |
|------|----------------|
| **Subject / publisher** | Holds subscribers; `emit(event, payload)` |
| **Observer / subscriber** | `handle(payload)` |
| **Event** | Named fact (`LaunchEvents.Succeeded`) |

## Core idea

…

## Variations / implementations

…

## Standard config / commands

```typescript
type Handler<T> = (payload: T) => void | Promise<void>;

class LaunchEventBus {
  private handlers = new Map<string, Set<Handler<any>>>();

  subscribe<T>(event: string, handler: Handler<T>) {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)!.delete(handler);
  }

  async emit<T>(event: string, payload: T) {
    const set = this.handlers.get(event);
    if (!set) return;
    for (const h of set) await h(payload);
  }
}

const bus = new LaunchEventBus();

// extension seam — new side-effect
bus.subscribe('launch.succeeded', async (p) => {
  await metrics.increment('launch.ok', { platform: p.platform });
});

bus.subscribe('launch.succeeded', async (p) => {
  await audit.write({ type: 'launch', id: p.campaignId });
});
```

### Extending

New launch side-effect → `launchEventBus.subscribe(LaunchEvents.*, …)`. Do not edit the pipeline for every notifier.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Side-effect failure rolls back launch | Observer in critical path | Emit after commit; make handlers best-effort or outbox |
| Subscriber never fires | Wrong event name / subscribe after emit | Central event constants; subscribe at boot |
| Ordering assumptions | Set iteration order | Do not rely on order; or use explicit pipeline step |
| Memory leak | Forgotten unsubscribe in hot paths | Return disposer; clear on shutdown |

## Gotchas

> [!WARNING]
> If a "subscriber" is required for correctness (must create billing record), it is **not** a side-effect — put it in the Template Method steps or outbox with retry.

- Observer ≠ Command — command is intent to do; event is fact that happened.
- Sync `emit` awaiting all handlers can stall requests — prefer queue for slow IO ([[Messaging/Web hooks]]).

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- One caller, one reaction — plain function call.
- Need guaranteed transactional coupling — same unit of work, not bus.

## Related

[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Template Method]] [[Design pattern/Mediator]] [[Messaging/Web hooks]] [[DevOps/Slack]]
