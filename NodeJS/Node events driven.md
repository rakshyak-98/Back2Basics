[[NodeJS]] [[EventEmitter]] [[Event Loop]] [[event emitter]] [[Stream Events]]

# Node events driven

> Node’s core style — emit events, run listeners; `http`/`fs`/`stream` already use `EventEmitter` under the hood.





## Interview Relevance
Interviewers use **Node events driven** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **on / emit**, **once**, **Built-ins**.

## Sources
- [Wikipedia — Node events driven](https://en.wikipedia.org/wiki/Node_events_driven) — overview

## Key Concepts
- **on / emit:** Subscribe / publish — Observer pattern in core.
- **once:** Single-shot listener — First connect, handshake done.
- **Built-ins:** http, fs, stream — You already write event-driven code.

## Technical Details
```txt
ee.on('login', cb)  …  ee.emit('login', user) → cb(user)
```

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

## Real-World Applications
In production APIs and tooling, **Node events driven** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`error` is special** — no listener ⇒ thrown / process abort paths; **Sync emit** — listeners run immediately on the stack; heavy work blocks the loop.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node’s core style — emit events, run listeners; `http`/`fs`/`stream` already use…).
- **Con / when not:** **Request/response RPC** — promises/async APIs clearer than ad-hoc events.
- **Con / when not:** **Cross-process** — need IPC/queue, not in-process emitters.

## Comparison
vs [[EventEmitter]]: know when each applies — do not treat them as interchangeable. vs [[Event Loop]]: know when each applies — do not treat them as interchangeable. vs [[event emitter]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`error` is special** — no listener ⇒ thrown / process abort paths.
- **Sync emit** — listeners run immediately on the stack; heavy work blocks the loop.
- **Memory climb:** check Listeners never removed; fix: `off` on cleanup
- **MaxListeners warning:** check Accidental re-subscribe; fix: Subscribe once; remove on destroy
- **Crash on emit:** check `error` with no listener; fix: Always `.on('error', …)`
- **Missed first event:** check Subscribed too late; fix: Emit after listeners; or buffer
