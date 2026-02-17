```js
let buffer = new ArrayBuffer(16):
console.log(buffer.byteLength); // output 16
```

### Copy content of one file to another 

- create readable stream fro the file `input.txt` and reads the file in chunks instead of loading the whole file into memory at once.

```js
const fs = require('fs');

const readable = fs.createReadStream('input.txt', { highWaterMark: 16 * 1024 });
const writable = fs.createWriteStream('output.txt');

readable.pipe(writable);

readable.on('error', err => console.error('Read error:', err));
writable.on('error', err => console.error('Write error:', err));

writable.on('finish', () => {
  console.log('File copy completed successfully');
});
```

- `highWaterMark` controls buffer size (default: `64KB` for files, `16KB` for sockets).

- `redable.pipe(writable)` -> connects the two stream using `.pipe()`
	- Readable stream reads a chunk (up to 16 KB) from `input.txt`
	- Automatically writes that chunk to `writable` stream.
	- When writable is busy (buffer full), readable resumes.
	- Repeats until the entire file is copied.
	- When readable ends -> automatically calls `writable.end()` -> close output file cleanly.

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

### How does the `byteLength` is calculated
the `.byteLength` of an `ArrayBuffer` or a TypedArray in JavaScript is calculated based on the total number of bytes allocated in memory when `ArrayBuffer` is created.

#### TypedArray `.byteLength`
- for TypedArray (e.g., `Uint8Array` `Float32Array`) `.byteLength` is calculated as

```txt
byteLength = number of elements x bytes per element
byteLength = length x BYTES_PER_ELEMENT

```
```js
console.log(Float32Array.BYTES_PER_ELEMENT); // ouptut 4
console.log(new Float32Array(5).byteLength); // output 5 x 4 = 20
```

### Convert buffer to string

```js
fs = require('fs');

fs.readdirSync("./");
file = fs.readfileSync("./img.png");
Buffer.isBuffer(file);

file.toString("base64");

```