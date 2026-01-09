Inter Process Communication namespace isolate process from [[Sysv]] style inter-process communication. 
- This prevents process in different IPC namespaces from using.

IPC -> pipes, sockets, shared memory, signals

> [!INFO]
> Requires kernel mediation, context switches, data marshaling.