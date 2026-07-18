CPU-bound -> your CPU is the one sweating
IO-bound -> your CPU is mostly sitting and waiting for someone/something else.
CPU-bound task and IO-bound tasks are two fundamentally different types of **Workloads** that behave very differently when it comes to performance, concurrency, threading, asyncio, multiprocessing etc.

|Aspect|CPU-bound task|IO-bound task|
|---|---|---|
|Main bottleneck|CPU (computation)|Waiting for I/O (disk, network, database, API)|
|What the program spends most time doing|Doing calculations, processing data|Waiting (sleeping / blocked)|
|Typical examples|• Video encoding / transcoding • Machine learning training / inference • Image processing (filters, resizing) • Scientific simulations • Cryptography / hashing • Complex mathematical computations • Compression / decompression|• Serving web requests • Reading/writing large files • Database queries • Making HTTP API calls • Downloading / uploading files • Waiting for user input • Network communication (sockets) • Reading logs / streaming data|
|Threading helps?|Usually **no** (or very little)|**Yes** — very effective|
|Multiprocessing helps?|**Yes** — usually the best solution|Helps sometimes, but often overkill|
|asyncio / async-await helps?|Usually **no** or very little|**Yes** — often excellent solution|
|GIL impact (in Python)|Severe limitation — only one thread makes progress|Almost no impact — threads can wait in parallel|
|Typical scaling strategy|• More CPU cores • Multiprocessing • Faster CPU • Optimize algorithm|• More concurrent connections • Async I/O • Connection pooling • Caching|
|Real-world feel|8-core CPU → can run ~8 such tasks efficiently at the same time|8-core CPU → can easily handle hundreds or thousands of such tasks concurrently|


## Why mixing CPU-bound + IO-bound tasks in one shared thread pool causes serious problem

- The CPU-bound tasks hog the threads -> IO-bound tasks get queued even though many threads are actually idle but blocked on I/O
