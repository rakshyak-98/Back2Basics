A **distributed system** is a system whose components are located on different network computers, which communicate and coordinate their actions by passing messages to one another.
significant challenges:
1. maintaining concurrency of components
2. overcoming the [lack of a global clock](#Clock Synchronization)

## Clock synchronization
is a topic of computer science and engineering that aims to coordinate otherwise independent clocks.
- real clocks will differ after some amount to time due to clock drift.
> [!Note] clock drift random number
> Computer clock drift can be utilized to build random number generators. These can however be exploited by timing attacks.

## Clock drift
- clock does not run at exactly the same rate as a reference clock.
- gradually desynchronises from other clock.
- computer requires some synchronization mechanism for any high-speed communication.

# Reference
- [clock drift](https://en.wikipedia.org/wiki/Clock_drift)
- [clock synchronization](https://en.wikipedia.org/wiki/Clock_synchronization)
- [distributed computing](https://en.wikipedia.org/wiki/Distributed_computing)
- 
