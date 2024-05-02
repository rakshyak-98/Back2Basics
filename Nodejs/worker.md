- feature introduced in Node.js
- enable concurrent execution of JavaScript code within a single process.
- workers allow you to run code in separate threads.
	- beneficial for tasks that are CPU-intensive or I/O bound.
	- applications need to perform multiple tasks simultaneously without blocking the main event loop.
> [!NOTE] networking I/O operations use **main thread** except of DNS.