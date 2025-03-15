`pipe()` is used in NodeJS streams to read from a readable stream and write to a writable stream efficiently.
```js
const fs = require("fs");

const readable = fs.createReadStrema('input.txt');
const writable = fs.createWriteStream('output.txt')

readable.pipe(writable);
```
- handles backpressure automatically

#### Chaining pipes
```js
const zlib = require("zlib");

fs.createReadStream('intput.txt')
	.pipe(zlib.createGzip()) // compress
	.pipe(fs.createWriteStream('output.txt.gz')) // write to file

```
- streams can be chained for transformation (e.g., compression);

```js
const http = require("http");
const fs = require("fs");

http.createServer((req, res) => {
	fs.createReadStream('index.html').pipe(res);
}).listen(3000);

```
- serves `index.html` file over HTTP efficiently

```js
readable.pipe(writable).on('error', (err) => {
	console.error("Error", err);
})

```
- Ensure error handling to prevent crashes