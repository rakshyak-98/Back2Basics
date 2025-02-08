```txt
TypeError: The "chunk" argument must be of type string or an instance of Buffer or Uint8Array. Received type number (137)
    at new NodeError (node:internal/errors:405:5)
    at _write (node:internal/streams/writable:315:13)
    at WriteStream.Writable.write (node:internal/streams/writable:337:10)
    at pumpToNode (node:internal/streams/pipeline:136:21)
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
[ERROR] 13:58:25 TypeError: The "chunk" argument must be of type string or an instance of Buffer or Uint8Array. Received type number (137)
```

 the error occurs because `Readable.from(file.buffer)` is incorrect. The `file.buffer` is already a `Buffer`, and `Readable.from` expects an array of buffers or strings.