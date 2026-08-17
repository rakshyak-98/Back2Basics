[[NodeJS]] [[Event Loop]] [[Stream]] [[Node events driven]] [[worker threads]] [[web workers]]

# EventEmitter

> EventEmitter is Node.js's built-in publish-subscribe primitive — objects emit named events and registered listeners run synchronously in registration order when the event fires.

---

## Why It Matters

`EventEmitter` is the backbone of Node's I/O APIs: `net.Socket`, `http.Server`, `fs.ReadStream`, and `process` all extend it. Understanding synchronous listener execution, the special `error` event, and listener leak patterns explains production bugs like memory growth over days, uncaught exceptions from async listeners, and HMR duplicating handlers in development.

---

## Sources

- [Node.js — Events / EventEmitter](https://nodejs.org/api/events.html) — Official API reference for `on`, `once`, `emit`, `removeListener`, `setMaxListeners`, and async listener behavior.
- [Node.js — Error handling](https://nodejs.org/api/errors.html#errors) — How unhandled `error` events crash the process and best practices for attaching error listeners.
- [Wikipedia — Observer pattern](https://en.wikipedia.org/wiki/Observer_pattern) — Design pattern context: subject notifies observers without tight coupling.

---

## Key Concepts

```txt
Producer                    EventEmitter                    Listeners
   │                              │                              │
   └── emit('data', chunk) ──────►│──► on('data') handler 1      │
                                  │──► on('data') handler 2      │
                                  └──► once('end') handler       │
```

| Property | Detail |
|----------|--------|
| **Synchronous dispatch** | All listeners for an event run before `emit()` returns — a slow listener blocks others. |
| **`error` is special** | `emit('error')` with no listener throws — crashes the process. |
| **Order** | Listeners run in registration order; `prependListener` inserts at front. |
| **Leak pattern** | `on()` without matching `removeListener` / `off()` keeps closures alive. |
| **Built-in extenders** | Streams, HTTP, TCP sockets, child processes — all EventEmitter subclasses. |

---

## Technical Details

### Basic usage

```javascript
import { EventEmitter } from 'node:events';

const emitter = new EventEmitter();

emitter.on('job', (id) => console.log('processing', id));
emitter.once('ready', () => console.log('fires once only'));

emitter.emit('job', 42);
emitter.emit('ready');
```

### Class extension pattern

```javascript
class JobQueue extends EventEmitter {
  constructor() {
    super();
    this.setMaxListeners(20); // raise default 10 if many modules attach
  }

  enqueue(job) {
    this.emit('enqueued', job);
    this.process(job);
  }

  process(job) {
    this.emit('progress', 50);
    this.emit('done', job);
  }
}
```

### Streams (built-in emitter)

```javascript
import { createReadStream } from 'node:fs';

const reader = createReadStream('large-file.bin');
reader.on('data', (chunk) => { /* handle backpressure with pause/resume */ });
reader.on('end', () => console.log('complete'));
reader.on('error', (err) => console.error(err)); // always attach
```

### Listener management

```javascript
emitter.once('open', handler);           // auto-removed after first fire
emitter.off('data', handler);            // alias for removeListener
emitter.removeAllListeners('data');      // nuclear option for one event
emitter.listenerCount('data');           // debug duplicate registrations
```

### Async listener errors (Node 16+)

```javascript
emitter.on('data', async () => {
  throw new Error('boom'); // rejected promise → 'error' event if unhandled
});
emitter.on('error', (err) => console.error('caught:', err.message));
```

### Failure signals

| Symptom | Cause | Fix |
|---------|-------|-----|
| `MaxListenersExceededWarning` | Too many `on()` for same event | `setMaxListeners`; check for leaks |
| Memory grows over days | Listeners not removed | `off()` in cleanup; WeakRef patterns |
| Uncaught exception crash | `emit('error')` without listener | Always attach `error` handler on streams |
| Handler fires twice after HMR | Hot reload re-registers | `removeAllListeners` before re-attach |
| Handler never runs | Event name typo | Log `emitter.eventNames()` |

---

## Mistakes to Avoid

- Assuming listeners run asynchronously — they block the emitter's caller.
- `emit('error')` without an `error` listener on any EventEmitter — process crash.
- Using arrow functions when you need `this` bound to the emitter in a class method listener.
- Registering the same listener on every HMR cycle without cleanup.
- Using EventEmitter as a global application state bus — untraceable data flow; prefer explicit APIs.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Decouples producers from consumers | Synchronous listeners block each other |
| Native to all Node I/O APIs | Easy to leak listeners |
| Simple API — `on` / `emit` | Not for request/response with one caller (use Promises) |
| | Not for cross-process messaging (use IPC, queues) |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[Event Loop]] | Event loop schedules I/O callbacks; EventEmitter is the in-process dispatch mechanism |
| [[Stream]] | Streams extend EventEmitter and add backpressure semantics |
| [[worker threads]] | Cross-thread messaging uses `postMessage`, not EventEmitter |
| Promises / async-await | Single consumer, structured error propagation |

---

## Use cases

- Custom job queue emitting `progress` and `done` events for CLI tooling.
- Wrapping a third-party SDK that uses callbacks into an EventEmitter interface.
- Debugging stream pipelines by attaching temporary `data`/`end`/`error` listeners.
