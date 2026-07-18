- The buffer cache is a [[kernel subsystem]] that manages buffers in memory to optimize disk I/O performance.
####  Some key points about the buffer cache 
- It maintains a set of buffer heads describing the buffers in the cache. 
- it uses a hash table to quickly find the [[buffer head]] for a given device and block number.
- Buffers are allocated on demand from free memory when needed.
- Dirty buffers (modified in memory) are written to disk at regular intervals to minimize I/O impact on user processes.