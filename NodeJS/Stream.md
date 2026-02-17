- Non-blocking and memory efficient for large file transfers.
- Handles large payloads without buffering entire data.
- Supports real-time streaming like live audio/video processing.

- four types of streams to handle data read and write operation, useful for handling large data sets without loading everything into memory.

> [!INFO] NodeJS streams use internal buffers to handle data efficiently.
> - Streams read/write chunks of data instead of loading everything into memory.
> - NodeJS maintains an internal buffer to balance the data flow (handle backpressure).

### Readable stream
- used to read data from the source
```javascript
const fs = require('fs')
const readStream = fs.createReadStream('file.txt')
readStrema.on('data', (chunk) => {
	console.log(chunk)
})

```
### Writable stream
- used to write data to destination
```javascript
const fs = require('f')
const writeStream = fs.createWriteStream('output.txt')
writeStream.write('hello world')
writeStream.end()

```
### Duplex stream
- Acts as both readable and writable streams
- inherit both readable and writable methods
```javascript
const { Duplex } = require('strema')
const duplex = new Duplex({
	read(size) {
			this.push('hello')
			this.push(null) // no more data
	},
	write(chunk, encoding, callback){
		console.log(chunk.toString())
		callback();
	}
})
duplex.write('hello, Duplex strema')

```
### Transform stream
- Special form of Duplex stream that can modify or transform the data as it is read or written
- inherits from Duplex, with added transformation logic.
```javascript
const { Transform } = require('stream')
const transform = new Transform({
	transform(chunk, encoding, callback){
		this.push(chunk.toString().toUpperCase())
		callback()
	}
})
process.stdin.pipe(transform).pipe(process.stdout)

```

- the most efficient way to handle I/O operation is in real time, consuming the input as soon as it is available and sending the output as soon as the application produces it.

> [!INFO]
> Blob -> Binary Large Object. Is a data type used to store large amounts of binary data, such as images, videos, audio, or other multimedia files, typically in database or file systems.

> [!NOTE]
> In javascript and web APIs, a blob represents immutable, raw data that can be read as text or binary and is commonly used for handling files and binary content in web application.

## Buffering vs Streaming

- **buffer mode** causes all the data coming from a resource to be collected into a buffer until the operation is completed, it is then passed back to the caller as one single blob of data.

**Example**: at time `t1`, some data is received from the resource and saved into the buffer. At time _t2_, another data chunk is received—the final one—which completes the read operation, so that, at _t3_, the entire buffer is sent to the consumer.
- **Stream** allow us to process the data as soon as it arrives from the resource.
	- program run in constant memory utilisation.

> [!INFO] Buffers in V8 are limited in size. You cannot allocate more than a few gigabytes of data.
```javascript
import buffer from "node:buffer"
console.log(buffer.constants.MAX_LENGTH)
```

#### Using buffer

```javascript
const zlib = require("node:zlib");
const { promisify } = require("node:util");
const {promises: fs} = require("node:fs");

const gzipPromise = promisify(zlib.gzip);
const filename = process.argv[2];

async function main() {
  const data = await fs.readFile("./.env");
  const zippedData = await gzipPromise(data);
  await fs.writeFile(`${filename}.gz`, zippedData);
  console.log("Done");
}

main();
```

#### Using stream

```javascript
const { createReadStream, createWriteStream } = require("node:fs");
const { createGzip } = require("node:zlib");
  
const filename = process.argv[2];
createReadStream(filename)
  .pipe(createGzip())
  .pipe(createWriteStream(`${filename}.gz`))
  .on("finish", () => console.log("Done"));
```

### Count the size of the chunk

```js

```