- designed to build scalable network application.
- because on non-blocking operations Scalable systems are very reasonable to develop in NodeJS.
- As an asynchronous event-driven JavaScript [[runtime environment]]. NodeJs is designed to build scalable network application.
- since their is no locks. NodeJS is free from dead-locking the processes.
- No function is NodeJS perform direct I/O.
- upon each connection, the callback is fired, but if there is no work to be done, NodeJs will sleep.
all of the I/O methods in the NodeJs standard library provide asynchronous versions, which are [[non-blocking]] and accept callback function.
- some methods have [[blocking]] counterparts, which have names that end with `Sync`.
### Topics
[[Blocking Vs Non-Blocking]]
[[Concurrency]] and [[Throughput]]
[[Event Loop]]
[[Callback]]