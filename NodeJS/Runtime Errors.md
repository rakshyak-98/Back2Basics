
```text
await is only valid in async functions and the top level bodies of modules
```

- This error occurs because you are trying to use `await` inside a standard JavaScript file that isn't wrapped in an `async` function or defined as an **ES Module**.
- **Top-Level Await in CommonJS**: Trying to use `await` at the top level of a file using `require()`. In Node.js, `require` (CommonJS) does not support top-level await; only `import` (ES Modules) does.

---

```text
ReferenceError: __dirname is not defined in ES module scope
```

- `__dirname` is not defined in ESM `__direname` and `__filename` do not exist. If you use them for `path.json` you must define them manually.

```js
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

- In ES modules, `__direname` and `__filename` are not available by default. You have to reconstruct them using `import.meta.url`

- CommonJS -> NodeJS wraps each file in a function that provides `__dirname` as an argument.
- ES Modules -> Files are treated as modules with a URL-based system `file://`. Since a URL is not a file system path, NodeJS provides `import.meta.url` instead, which must be converted to a path.

---

```text
Nginx configuration failed with message: Command failed: sudo nginx -t sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper sudo: a password is required
```

- this happens because your deployment script is running `sudo nginx -t` in a non-interactive environment (no terminal/TTY), but the user executing the command require a password for `sudo` and has no way to provide it automatically

---


`ReferenceError: Must call super constructor in derived class before accessing 'this' or returning from derived constructor`
- this comes when you access `this.constructor.name` before calling `super(message)`

```js
class AppError extends Error {
  constructor(statusCode, message, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.message = message;
    this.isOperational = isOperational;
  }
}

class BadRequestError extends AppError {
  constructor(message = "Bad Request") {
    this.name = this.constructor.name; // this line caused the error
    super(400, message);
  }
}

try {
  throw new BadRequestError("Missing hotel name");
} catch (error) {
  console.error(error.name);
  console.error(error.message);
  console.error(error.statusCode);
  console.log(error.stack);
}

```