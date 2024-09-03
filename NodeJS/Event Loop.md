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