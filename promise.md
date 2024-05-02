Why to switch to the promise-based API
- `async` `await` it's harder to create the kind of [[race condition]].
- with callback-based code, it's not only harder to figure out the order of code execution, it's also harder to control the order. Callback are harder to read and more error-prone to write.
- [[backpressure]] is naturally present when using the promise-based style.