[[NodeJS]] [[Event Loop]] [[Stream]] [[Node events driven]]

# EventEmitter

> One-line: pub/sub inside a Node process — decouple producers from listeners; foundation of streams, HTTP, and most core APIs.

## Mental model

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

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `MaxListenersExceededWarning` | `emitter.listenerCount('event')` | Fix leak; `removeListener`; or raise `setMaxListeners` after root-cause fix |
| Memory grows over days | Heap snapshot; count listeners on long-lived sockets | Remove listeners on `close`; use `once`; destroy streams |
| Handler never runs | Wrong event name typo | Log `emitter.eventNames()` |
| Uncaught exception crashes process | Missing `error` listener on emitter | Always `on('error', …)` for streams/sockets |
| Event order surprises | Sync handlers + microtasks | Document order; defer heavy work with `setImmediate` |
| Duplicate handlers after HMR | Hot reload re-registers `on` | `off` before `on`; use `once` for setup |

## Gotchas

> [!WARNING]
> **Listeners are synchronous** — CPU-heavy handler blocks I/O for all connections on that thread.

> [!WARNING]
> **`emit('error')` without listener throws** — attach `error` handler or use `{ captureRejections: true }` patterns for async.

> [!WARNING]
> **Arrow functions as listeners** — can't `removeListener` unless same reference stored.

> [!WARNING]
> **Don't emit during `removeListener`** — mutating listener list while iterating causes skipped/duplicate calls.

## When NOT to use

- **Cross-process messaging** — use [[child process]] IPC, Redis pub/sub, or a message broker.
- **Request/response with one caller** — Promises/async functions are clearer than emit/wait hacks.
- **Global event bus for all app state** — becomes undebuggable; prefer explicit DI or state store.

## Related

[[event emitter]] [[Event Loop]] [[Stream]] [[Node events driven]] [[worker threads]]
