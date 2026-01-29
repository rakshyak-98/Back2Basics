```js
fs = require("fs");
fs.readdirSync("."); // get list of files in current path 
```

> [!INFO]
> if no-encoding is passed then you will get a buffer.
```js
fs.readFile("file.txt", "utf8", (err, data) => {
	console.log(data);
	console.log(data.split("\n")):
})
```