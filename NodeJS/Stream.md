- four types of streams to handle data read and write operation, useful for handling large data sets without loading everything into memory
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