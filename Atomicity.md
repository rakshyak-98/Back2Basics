
Multithreaded programming Atomicity: if one thread executes an atomic operation, that means there is no way that another thread could see the half-finished result of the operation. The system can be only in the state it was before the operation or after the operation, not something in between.

ACID Atomicity: describes what happens if a client wants to make several writes, but a fault occurs after some of the writes have been processed. For example a process crashes, a network connection is interrupted, a disk becomes full, or an integrity constraint is violated.