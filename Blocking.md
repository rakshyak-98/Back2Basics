- execution of additional JavaScript in the NodeJs process must wait until a non-JavaScript operation completes.
**non-JavaScript operations**: like reading or writing data to a file, making a network request, reading or persisting data to a database.

> [!NOTE] INFO
> in the synchronous version if an error is thrown it will need to be caught or the process will crash. In the asynchronous version, it is up to the author to decide whether an error should throw as shown.
