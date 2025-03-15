
```js
const fs = require('fs');

const readable = fs.createReadStream('input.txt', { highWaterMark: 16 * 1024} )
const writable = fs.createWritableStream('output.txt');

redable.pipe(writable);
```
- `highWaterMark` controls buffer size (default: `64KB` for files, `16KB` for sockets).

#### Buffer status
```js
const stream = fs.createWritableStream('output.txt');

const canWrite = stream.write(Buffer.alloc(1024));
console.log("Can write more ?", carWrite);

if (!stream.write(data)){
	stream.once('drain', () => {
		console.log("Buffer drained, writing more data...");
	})
}

```
- if `write()` returns `false`, the internal buffer is full (wait for `drain` event).

> [!INFO] consumers and streams
> - Large files -> Control buffer size to avoid memory issues.
> - Slow consumers -> Backpressure prevents overload.
> - Socket streams -> Use small buffers for real-time data transfer.