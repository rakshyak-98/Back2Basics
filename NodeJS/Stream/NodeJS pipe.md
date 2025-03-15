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
```