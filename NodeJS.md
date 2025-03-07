- child process can  be spawned by using `child_process.fork()` API (instead of using multiple threads).
- `cluster` module allows you to share sockets between processes to enable load balancing over your cores.
- designed to build scalabel network application ([[non-blocking]], [[Asynchronous]], [[Event Loop]]).
- because on non-blocking operations Scalabel systems are very reasonable to develop in Node.js.
- As an asynchronous event-driven JavaScript [[runtime environment]]. Node.js is designed to build scalabel network application.
- since their is no locks. Node.js is free from dead-locking the processes.
- No function is Node.js perform direct I/O.
- upon each connection, the callback is fired, but if there is no work to be done, Node.js will sleep.
all of the I/O methods in the Node.js standard library provide asynchronous versions, which are [[non-blocking]] and accept callback function.
- some methods have [[blocking]] counterparts, which have names that end with `Sync`.
- you can run experimental features by running Node.js with flags.
- instead of blocking the thread and wasting CPU cycles waiting, Node.js will resume the operations when the response comes back. This helps Node.js to handle thousands of concurrent connections with a single server without introducing the burden of managing thread concurrency, which could be a significant source of bugs.
- In the browser environment, all JavaScript files included in a webpage share the same global namespace. In Node.js or other server-side environments, each file has its own module-level scope, but variables declared without `var` `let` or `const` are still added to the global namespace.
### Node.js in production and development
- put `NODE_ENV=production` in `.bash_profile` with the Bash shell, persist in case of a system restart.

```javascript
if (process.env.NODE_ENV == 'development') {
	app.use(express.errorHandler({dumpExceptions: true, showStack: true}))
}

if (['production', 'staging'].includes(process.env.NODE_ENV)){
	app.use(express.errorHandler());
}
```

## Difference Between Node.js and Browser

| Node.js                                               | browser                                    |
| ----------------------------------------------------- | ------------------------------------------ |
| frontend and backend in a single language             |                                            |
| don't have `document` `window` object                 | interacting with the DOM or other Web APIs |
| Node.js provide additional API like filesystem access |                                            |
| Node.js support both CommonJS and ES module systems   | browser have ES module                     |

> [!NOTE] Memory leaks happen when a program allocates memory but does not release it with it is no longer needed.
- memory leaks happens due to use of [[closure]] [[circular references]] [[global variables]].
## Asynchronous control flow patterns with callback
- Asynchronous code can make it hard to predict the order in which statements are executed.
### Reference 
[learn node js](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
[[Blocking Vs Non-Blocking]]
[[Concurrency]] and [[Throughput]]
[[Event Loop]]
[[Callback]]