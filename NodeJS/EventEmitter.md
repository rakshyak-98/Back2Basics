[[NodeJS]] [[Event Loop]] [[Stream]] [[Node events driven]] [[event emitter]] [[worker threads]]

# EventEmitter

> Node’s observer bus — `emit` named events; listeners run synchronously in registration order.

## Interview Relevance

Interviewers probe **EventEmitter** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — Events / EventEmitter](https://nodejs.org/api/events.html) — deep-dive
- [Wikipedia — EventEmitter](https://en.wikipedia.org/wiki/EventEmitter) — overview

## Core Definition

`EventEmitter` is Node's observer pattern: objects **emit** named events; registered listeners run synchronously in registration order (unless `setImmediate`/`async` inside handler).

## Key Concepts

- `EventEmitter` is Node's observer pattern: objects **emit** named events; registered listeners run synchronously in registration order (unless `setImmediate`/`async` inside hand…
- Core APIs extend `EventEmitter`: `net.Socket`, `http.Server`, `fs.ReadStream`, `process`. Listener leaks (`on` without `removeListener`) are a top cause of memory growth in long…
- **Sync by default:** a slow listener blocks other listeners and the emitter's caller until it returns.

## Technical Details

`EventEmitter` is Node's observer pattern: objects **emit** named events; registered listeners run synchronously in registration order (unless `setImmediate`/`async` inside handler).

```
Producer                    EventEmitter                    Listeners
   │                              │                              │
   └── emit('data', chunk) ──────►│──► on('data') handler 1      │
                                  │──► on('data') handler 2      │
                                  └──► once('end') handler       │
```

Core APIs extend `EventEmitter`: `net.Socket`, `http.Server`, `fs.ReadStream`, `process`. Listener leaks (`on` without `removeListener`) are a top cause of memory growth in long-lived servers.

**Sync by default:** a slow listener blocks other listeners and the emitter's caller until it returns.

### Basic usage

```javascript
import { EventEmitter } from 'node:events';

class JobQueue extends EventEmitter {}
const queue = new JobQueue();

queue.on('job', (id) => console.log('processing', id));
queue.once('ready', () => console.log('first boot only'));

queue.emit('job', 42);
```

### Extend EventEmitter (class pattern)

```javascript
import { EventEmitter } from 'node:events';

class MyService extends EventEmitter {
  constructor() {
    super();
    this.setMaxListeners(20); // raise if many modules attach
  }

  doWork() {
    this.emit('progress', 50);
    this.emit('done');
  }
}
```

### Streams (built-in emitter)

```javascript
import { createReadStream } from 'node:fs';

const reader = createReadStream('large-file.bin');

reader.on('data', (chunk) => { /* backpressure: pause if slow consumer */ });
reader.on('end', () => console.log('complete'));
reader.on('error', (err) => console.error(err)); // always attach error handler
```

### `once`, `off`, `prependListener`

```javascript
emitter.once('open', handler);           // auto-removed after first fire
emitter.off('data', handler);            // same as removeListener
emitter.prependListener('data', first);  // runs before older listeners
```

### Async listener errors (Node 16+)

```javascript
emitter.on('data', async () => {
  throw new Error('boom'); // surfaces as 'error' on emitter if unhandled
});
emitter.on('error', (err) => console.error(err));
```

## Real-World Applications

In production APIs and tooling, **EventEmitter** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Listeners are synchronous** — CPU-heavy handler blocks I/O for all connections on that thread; **`emit('error')` without listener throws** — attach `error` handler or use `{ captureRejections: true }` patterns for async.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (EventEmitter — └── emit('data', chunk) ──────►│──► on('data') handler 1 │).
- **Con / when not:** **Cross-process messaging** — use [[child process]] IPC, Redis pub/sub, or a message broker.
- **Con / when not:** **Request/response with one caller** — Promises/async functions are clearer than emit/wait hacks.
- **Con / when not:** **Global event bus for all application state** — becomes undebuggable; prefer explicit DI or state store.

## Comparison

vs [[Event Loop]]: know when each applies — do not treat them as interchangeable. vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[Node events driven]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Listeners are synchronous** — CPU-heavy handler blocks I/O for all connections on that thread.
- **`emit('error')` without listener throws** — attach `error` handler or use `{ captureRejections: true }` patterns for async.
- **Arrow functions as listeners** — can't `removeListener` unless same reference stored.
- **Don't emit during `removeListener`** — mutating listener list while iterating causes skipped/duplicate calls.
- **`MaxListenersExceededWarning`:** check `emitter.listenerCount('event')`; fix: Fix leak; `removeListener`; or raise `setMaxListeners` after root-cause fix
- **Memory grows over days:** check Heap snapshot; count listeners on long-lived sockets; fix: Remove listeners on `close`; use `once`; destroy streams
- **Handler never runs:** check Wrong event name typo; fix: Log `emitter.eventNames()`
- **Uncaught exception crashes process:** check Missing `error` listener on emitter; fix: Always `on('error', …)` for streams/sockets
- **Event order surprises:** check Sync handlers + microtasks; fix: Document order; defer heavy work with `setImmediate`
- **Duplicate handlers after HMR:** check Hot reload re-registers `on`; fix: `off` before `on`; use `once` for setup
