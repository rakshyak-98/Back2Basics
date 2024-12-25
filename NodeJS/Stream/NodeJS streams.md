- the most efficient way to handle I/O operation is in real time, consuming the input as soon as it is available and sending the output as soon as the application produces it.

## Buffering vs Streaming
- **buffer mode** causes all the data coming from a resource to be collected into a buffer until the operation is completed, it is then passed back to the caller as one single blob of data.
**Example**: at time _t1_, some data is received from the resource and saved into the buffer. At time _t2_, another data chunk is received—the final one—which completes the read operation, so that, at _t3_, the entire buffer is sent to the consumer.
- **Stream** allow us to process the data as soon as it arrives from the resource.
	- program run in constant memory utilizations.

> [!INFO] Buffers in V8 are limited in size. You cannot allocate more than a few gigabytes of data.
```javascript
import buffer from "node:buffer"
console.log(buffer.constants.MAX_LENGTH)
```

#### using buffer
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

#### using stream
```javascript
const { createReadStream, createWriteStream } = require("node:fs");
const { createGzip } = require("node:zlib");
  
const filename = process.argv[2];
createReadStream(filename)
  .pipe(createGzip())
  .pipe(createWriteStream(`${filename}.gz`))
  .on("finish", () => console.log("Done"));
```