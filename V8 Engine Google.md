"Why does NodeJS need to provide `fs`? Why can't v8 just have `readFile()`?"
- V8 doesn't know what a file is. it need to require knowledge of :
	- filesystem semantics
	- files
	- OS system calls
	- file descriptors
	- permissions
	- paths
	- etc.
These are not javascript language concepts.

"V8 understands javascript; NodeJS exposes capabilities that javascript can use."

```js
cosnt x = 10 + 20 /* V8 can handle */
fs.readFile("data.txt", callback) /* V8 can execute the Javascript call, but Nodejs provides the actual filesystem capability*/
```


