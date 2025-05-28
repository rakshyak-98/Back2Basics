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


```txt
> pipeline( fs.createReadStream(file), zlib.createGzip(), fs.createWriteStream(file.concat(".gz")));
Uncaught: TypeError [ERR_INVALID_ARG_TYPE]: The "streams[stream.length - 1]" property must be of type function. Received an instance of WriteStream at popCallback (node:internal/streams/pipeline:73:3) at pipeline (node:internal/streams/pipeline:181:37) { code: 'ERR_INVALID_ARG_TYPE' }
```
- Error happens because `stream.pipeline()` without Promise wrapper, which is required in its native form.

> [!NOTE]
> Stream pipeline expects a callback or you need to **promisify** it.
```js
const { pipeline } = require('stream');
const fs = require('fs');
const zlib = require('zlib');

pipeline(
  fs.createReadStream(file),
  zlib.createGzip(),
  fs.createWriteStream(file + '.gz'),
  (err) => {
    if (err) {
      console.error('Pipeline failed:', err);
    } else {
      console.log('Pipeline succeeded.');
    }
  }
);

```

```js
const { pipeline } = require('stream');
const { promisify } = require('util');
const fs = require('fs');
const zlib = require('zlib');

const pipelineAsync = promisify(pipeline); // promisify

await pipelineAsync(
  fs.createReadStream(file),
  zlib.createGzip(),
  fs.createWriteStream(file + '.gz')
);

```

> [!INFO]
> the last argument of `pipeline()` must be a function (callback) if not promisified. If you omit it, Node tries to treat your last stream as a callback, causing:
```txt
Uncaught: TypeError [ERR_INVALID_ARG_TYPE]: The "streams[stream.length - 1]" property must be of type function. Received an instance of WriteStream at popCallback
```