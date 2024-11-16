we can use stream methods like `read` and `write` in combination with stream event listeners to consume streams.
```javascript
readable.on('data', chunk => {
	writable.write(chunk);
})

readable.on('end', () => {
	writable.end();
})
```

> [!INFO] The rate at which data is pushed by or written to a stream is known as *pressure* of the stream.
- when a writable stream has a slower rate of processing data than the rate of a readable stream that's pushing data, data will start buffering in the writable stream. This is known as *backpressure*

> [!NOTE] As long as writable stream is operating within its memory limits, its `write` method will return `true`.
- when the memory limit is reached, the `write` method returns `false` to indicate that further attempts to write data tot he stream should stop until the `drain` event is emitted.

> [!NOTE] The `error` event may be emitted by streams at any time and should always be handled, even when using the `pipe` method.

```javascript
readable.pipe(writable);

readable.on('error', (err) => {
	// handle potential read errors
})

writable.on('error', (err) => {
	// handle potential write errors
})
```

## Paused and Flowing Modes
Readable streams have two main modes that affect the way we can consume them. They can be either in the paused mode, or in the flowing mode. These modes are sometimes referred to as pull and push modes.
- All readable streams start in the paused mode by default
- but they can be easily switched to flowing and back to paused when needed
- Sometimes, the switching happens automatically.
When a readable stream is in the paused mode, we can use the `read()` method to read from the stream on demand. However, for a readable stream in the flowing mode, the data is continuously flowing and we have to listen to events to consume it.

> [!NOTE] In the flowing mode, data can actually be lost if no consumers are available to handle it. This is why when we have a readable stream in flowing mode, we need a `data` event handler.

> [!INFO] When consuming readable streams using the `pipe` method, we don't have to worry about these modes as `pipe` manage them automatically.