a function executes only after a specific time has passed since its last invocation.

> [!INFO]
> Ensures limit to a function execution. Function only executed after a certain delay since the last call.

```js
function debounce(func, delay){
	let timer;
	return function (...args) {
		clearTimeout(timer);
		timer = setTimeout(() => func.apply(this, args), delay);
	}
}
```
- A search input box where logging occurs only after 300 ms of inactivity.