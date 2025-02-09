### Promisify 
```js
const util = require('utils')

function foo(callback){
	callback(null, "Hi, I'm Foo")	
}

const fooAsync = utils.promisify(foo)

fooAsync.then(res => {
	console.log(res)
})

```
- The `util.promisify()` is designed to work with callback-style functions