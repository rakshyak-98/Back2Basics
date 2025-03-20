-  order of execution of a set of asynchronous tasks is not important.
- the parallel execution task is carried out be an underlying, non-blocking API and interleaved by the event loop.

> [!INFO] a task gives control back to the event loop when it requests a new asynchronous operation, allowing the event loop to execute another task.
- this is *concurrency*

```js
const { exec } = require("child_process")

exec("ls -l", (error, stdout, stderr) => {
	console.log(stdout);
})

```
- use `exec` when you need shell features (e.g., `&&` `|` `*`)
- command are passed as a single string.

```js
const { exec } = require("child_process");

exec("echo Hello && ls -l", (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error.message}`);
        return;
    }
    console.log(`Output:\n${stdout}`);
});

```

> [!WARNING] if user input is included, it can lead to shell injection (e.g., `exec("rm -rf /")` if poorly sanitized)

```js
const { execFile } = require("child_process");

execFile("ls", ["-l"], (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error.message}`);
        return;
    }
    console.log(`Output:\n${stdout}`);
});

```
- arguments are passed as an array, preventing command injection
- faster and safer (no shell execution, prevents shell injection)
- best for running binaries or scripts with arguments.

### Force `exec` to use bash
```js
const { exec } = require("child_process");

exec("echo $0", { shell: "/bin/bash" }, (error, stdout) => {
    console.log(`Shell Used: ${stdout.trim()}`); // Output: /bin/bash
});

```