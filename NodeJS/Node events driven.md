[[NodeJS]] [[EventEmitter]] [[Event Loop]] [[EventEmitter]] [[Stream Events]]

# Node events driven

> Node’s core style — emit events, run listeners; `http`/`fs`/`stream` already use `EventEmitter` under the hood.

```txt
        Node events driven ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Node events driven** to check whether you can explain the …

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

## Mistakes to Avoid
- **Mistake:** **`error` is special**
- **Mistake:** **Sync emit**
- **Mistake:** **Memory climb:** check Listeners never removed
- **Mistake:** **MaxListeners warning:** check Accidental re-subscribe
- **Mistake:** **Crash on emit:** check `error` with no listener
- **Mistake:** **Missed first event:** check Subscribed too late

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node’s core style — emit events, run listeners; `http`/`fs`/`stream` already use…).
- **Con / when not:** **Request/response RPC**
- **Con / when not:** **Cross-process**

## Comparison
- vs [[EventEmitter]]: know when each applies


### Use cases
- In production APIs and tooling, **Node events driven** shows up whenever team…
