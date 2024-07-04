## NodeJs
- similar to `Web Worker` in browsers.
```javascript
const {Worker} = require('worker_threads');
const worker = new Worker("./worker.js');
```
- worker communicate with the main thread (and vice versa) using a messaging system. This is achieved through the `postMessage` method and the `onmessage` event handler.
```javascript
worker.postMessage({type: 'compute', data: someData});

const {parentPort, workerData} = require('worker_threads');

parentPort.on('message', (message) => {
	if(message.type === 'computer'){
		const result = performComputation(message.data);
		parentPort.postMessage({type: 'result', data: result});
	}
})
```
- each worker thread runs in isolation from the main thread and other worker threads. This allows tasks to be executed concurrently without blocking the event loop of the main thread.
- NodeJs mechanisms like `SharedArrayBuffer` and `Atomics` for sharing memory between worker threads, enabling efficient data exchange and synchronization.
- while `worker_threads` provide multi-threading capabilities, they are more heavyweight compared to browser web workers and may consume more resources. Therefor, their usage should be carefully considered based on the application's requirements and performance considerations.