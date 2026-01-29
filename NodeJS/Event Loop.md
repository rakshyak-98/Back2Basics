> [!INFO]
> - The event loop is libuv magic -> a single-threaded loop that processes queues of callback. It's why Node excels at I/O-heavy apps (e.g., APIs, streaming)

- single-threaded loop responsible for handling all asynchronous tasks.
- connecting the queue (micro and macro queue) to the call stack.
- a runtime construct instead of as a library.
- Node.js simply enters the event loop after executing the input script.
- Node.js *exit* the event loop when there are no more callbacks to perform.
- in other  systems, their is always a blocking call to start the event-loop.
- event loop is hidden from the user in browser.

The runtime pools for IO events from the OS, such as a new connection arriving, a socket becoming ready to read, or a timer expiring. Then the runtime reacts to the events and invokes the callbacks that the programmer registered earlier. This process repeats after all events have been handled, thus it's called the event loop.

> [!INFO] Event loop in Node.js as a runtime construct instead of as a library.

> [!INFO] in other system their is a blocking call to start the event-loop.

>[!INFO] single thread single compute blocks other.

### Concurrency in Node.js is Event-based
while an event handler is running, the single-threaded runtime cannot do anything for the other connections until the handler returns. The longer you process an event, the longer everything else is delayed.

## NodeJS Event loop has 6 phases

- iterated per "tick". Each phase handles specific callback types, and the loop blocks efficiently (e.g., via epoll on Linux) waiting to events

|Phase|What Happens|Examples|Why It Matters (Senior Insight)|
|---|---|---|---|
|**Timers**|Executes expired `setTimeout`/`setInterval` callbacks. (Min delay: 1ms due to loop overhead.)|`setTimeout(fn, 0)` runs here, but after current sync code.|Prioritizes time-based tasks; misuse (e.g., recursive timeouts) starves other phases—causes high latency.|
|**Pending Callbacks**|Handles OS-level I/O callbacks (e.g., TCP errors). Mostly internal.|libuv queues failed socket ops here.|Rare for user code, but debug here for network flakiness (e.g., ECONNREFUSED).|
|**Idle/Prepare**|Internal Node/libuv prep (e.g., garbage collection hints). Not user-facing.|Used by addons or internals.|Ignore unless hacking Node core; impacts perf in edge cases like high GC.|
|**Poll**|Waits for I/O events (e.g., new data on sockets). Blocks if no work elsewhere, but checks timers often.|`fs.readFile` callback lands here after libuv completes.|Core of non-blocking: Uses OS selectors (epoll/kqueue) for efficiency. Long polls = idle server; short = busy.|
|**Check**|Runs `setImmediate` callbacks. After poll, for "next tick" but post-I/O.|`setImmediate(fn)` for deferring without timeout.|Great for batching post-I/O work; faster than `process.nextTick` in loops.|
|**Close Callbacks**|Cleans up closed resources (e.g., socket 'close' events).|`socket.on('close', cleanup)`.|Ensures no leaks; forget this, and you'll OOM in prod.|

- Microtasks Queue -> Outside phases, but interleaved - `Promise` resolves or `process.nextTick` run immediately after current operation (before next phase). This is for error handling.

How it Ticks -> Loop runs until no more callbacks. libuv polls OS for events (e.g., via `epoll_wait` on Linux), then queues JS callbacks in V8. [article](https://nodevibe.substack.com/p/tcp-and-nodejs-server-internals-a)

- Blocking the Loop: Sync code (e.g., long for loop) starves the loop—everything waits. Fix: Break into async chunks.