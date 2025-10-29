- synchronisation tool for managing access to shared resources in concurrent systems (threads/processes).

> [!INFO]
> - integer variable used as a signal mechanism
> - Controlled by atomic operations `wait()` and `signal()`
> - Prevents race conditions, ensures mutual exclusion (mutex) or process coordination.

- a semaphore is a variable or [[ADT (Abstract Data Type)]] 
- used to *control access* to a common resource by multiple threads and avoid [[critical sections]] problems in a concurrent system such as a multitasking operating system.

### Binary semaphores
- used to implement locks