[[NodeJS]] [[Event Loop]] [[Stream]] [[Node events driven]] [[EventEmitter]] [[worker threads]]

# EventEmitter

> Node’s observer bus — `emit` named events; listeners run synchronously in registration order.

```txt
        EventEmitter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **EventEmitter** to see if you understand what it does ope…

## Sources
- [Node.js — Events / EventEmitter](https://nodejs.org/api/events.html) — deep-dive
- [Wikipedia — EventEmitter](https://en.wikipedia.org/wiki/EventEmitter) — overview

## Key Concepts
- **`EventEmitter` is:** `EventEmitter` is Node's observer pattern: objects **emit** named events
- **Core APIs:** Core APIs extend `EventEmitter`: `net.Socket`, `http.Server`, `fs.ReadStream`…
- **Sync by default:** a slow listener blocks other listeners and the emitter's caller until it retu…


- **Core:** `EventEmitter` is Node's observer pattern: objects **emit** named events

## Technical Details
- `EventEmitter` is Node's observer pattern: objects **emit** named events

```
Producer                    EventEmitter                    Listeners
   │                              │                              │
   └── emit('data', chunk) ──────►│──► on('data') handler 1      │
                                  │──► on('data') handler 2      │
                                  └──► once('end') handler       │
```

- Core APIs extend `EventEmitter`: `net.Socket`, `http.Server`, `fs.ReadStream`…
- Listener leaks (`on` without `removeListener`) are a top cause of memory grow…

- **Sync by default:** a slow listener blocks other listeners and the emitter's…

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

## Mistakes to Avoid
- **Mistake:** **Listeners are synchronous**
- **Mistake:** **`emit('error')` without listener throws**
- **Mistake:** **Arrow functions as listeners**
- **Mistake:** **Don't emit during `removeListener`**
- **Mistake:** **`MaxListenersExceededWarning`:** check `emitter.listenerCount(…
- **Mistake:** **Memory grows over days:** check Heap snapshot
- **Mistake:** **Handler never runs:** check Wrong event name typo
- **Mistake:** **Uncaught exception crashes process:** check Missing `error` li…
- **Mistake:** **Event order surprises:** check Sync handlers + microtasks
- **Mistake:** **Duplicate handlers after HMR:** check Hot reload re-registers …

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (EventEmitter — └── emit('data', chunk) ──────►│──► on('data') handler 1 │).
- **Con / when not:** **Cross-process messaging**
- **Con / when not:** **Request/response with one caller**
- **Con / when not:** **Global event bus for all application state**

## Comparison
- vs [[Event Loop]]: know when each applies


### Use cases
- In production APIs and tooling, **EventEmitter** shows up whenever teams ship…
