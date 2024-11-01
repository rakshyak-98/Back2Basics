-  order of execution of a set of asynchronous tasks is not important.
- the parallel execution task is carried out be an underlying, non-blocking API and interleaved by the event loop.

> [!INFO] a task gives control back to the event loop when it requests a new asynchronous operation, allowing the event loop to execute another task.
- this is *concurrency*