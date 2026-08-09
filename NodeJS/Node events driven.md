[[NodeJS]] [[EventEmitter]] [[Event Loop]] [[event emitter]]

# Node events driven

> Node’s core style — emit events, run listeners; `http`/`fs`/`stream` already use `EventEmitter` under the hood.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Register with `.on` / `.once`, fire with `.emit` — no waiting thread; the loop invokes listeners when the event fires.

```txt
ee.on('login', cb)  …  ee.emit('login', user) → cb(user)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **on / emit** | Subscribe / publish | “Observer pattern in core.” |
| **once** | Single-shot listener | “First connect, handshake done.” |
| **Built-ins** | http, fs, stream | “You already write event-driven code.” |

## Standard config / commands

```js
import { EventEmitter } from 'node:events'

const ee = new EventEmitter()
ee.on('userLogin', (user) => console.log(user.id))
ee.once('ready', () => console.log('once'))
ee.emit('userLogin', { id: 1 })
ee.emit('ready')
```

| Knob | Why it matters |
|------|----------------|
| `setMaxListeners` | Warn on leaks |
| Error event | Unhandled `error` can crash |
| `off` / `removeListener` | Prevent leaks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Memory climb | Listeners never removed | `off` on cleanup |
| MaxListeners warning | Accidental re-subscribe | Subscribe once; remove on destroy |
| Crash on emit | `error` with no listener | Always `.on('error', …)` |
| Missed first event | Subscribed too late | Emit after listeners; or buffer |

---

## Gotchas

> [!WARNING]
> **`error` is special** — no listener ⇒ thrown / process abort paths.

> [!WARNING]
> **Sync emit** — listeners run immediately on the stack; heavy work blocks the loop.

---

## When NOT to use

- **Request/response RPC** — promises/async APIs clearer than ad-hoc events.
- **Cross-process** — need IPC/queue, not in-process emitters.

---

## Related

[[EventEmitter]] [[event emitter]] [[Event Loop]] [[Stream Events]]
