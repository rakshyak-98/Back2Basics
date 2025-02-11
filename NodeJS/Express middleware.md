- They provide a way to execute code, modify the request and response objects, end the request-response cycle, and call the next middleware function in the stack.

### How middleware work
- middleware functions are executed sequentially in the order they are defined.
- middleware functions can perform tasks such as logging, authentication, parsing request bodies.
- they can modify the `req` and `res` object or end the request-response cycle by sending a response.

> [!NOTE] if a middleware function does not end the request-response cycle, it must call `next()` to pass control to the next middleware function.

1. Logging middleware
```js
const logger = (req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
};

export default logger;
```

2. Body parsing middleware
```js
import express from 'express';
import logger from './middleware/logger.js';

const app = express();

// Use JSON body parser middleware
app.use(express.json());

// Use custom logger middleware
app.use(logger);

// Example route
app.post('/data', (req, res) => {
    res.send(`Received data: ${JSON.stringify(req.body)}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
```

3. Authentication middleware
```js
const auth = (req, res, next) => {
    const token = req.header('Authorization');
    if (!token) {
        return res.status(401).send('Access denied. No token provided.');
    }
    // Verify token (pseudo-code)
    try {
        const decoded = verifyToken(token);
        req.user = decoded;
        next();
    } catch (ex) {
        res.status(400).send('Invalid token.');
    }
};

export default auth;
```

4. Error handling middleware
```js
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something went wrong!');
};

export default errorHandler;

```

5. Static file middleware
```js
import express from 'express';
import path from 'path';
import logger from './middleware/logger.js';
import errorHandler from './middleware/errorHandler.js';

const app = express();

// Use JSON body parser middleware
app.use(express.json());

// Use custom logger middleware
app.use(logger);

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Example route
app.post('/data', (req, res) => {
    res.send(`Received data: ${JSON.stringify(req.body)}`);
});

// Use error handling middleware
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
```

6. XSRF Token implementation
```js
// filepath: /home/ubuntu/GitHub/Playground/Javascript/src/index.js
const express = require('express');
const cookieParser = require('cookie-parser');
const csurf = require('csurf');

const app = express();

// Setup cookie parser middleware
app.use(cookieParser());

// Setup CSRF protection middleware
const csrfProtection = csurf({ cookie: true });

// Route to get CSRF token
app.get('/form', csrfProtection, (req, res) => {
   res.send(`<form action="/process" method="POST">
               <input type="hidden" name="_csrf" value="${req.csrfToken()}">
               <button type="submit">Submit</button>
             </form>`);
});

// Route to process form submission
app.post('/process', csrfProtection, (req, res) => {
   res.send('Form processed');
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Avoid Try-catch everywhere
```js
const asyncHandler = (fn) => (req, res, next) => {
	Promise.resolve(fn(req, res, next)).catch(next)
}
```

```js
const asyncHandler = require("@middleware/asychHandler")

app.get("/user", asyncHandler(async (req, res, next) => {
	const user = await User.findById(req.params.id);
	if(!user){
		throw new Error("User not found)
	}
	res.json(user);
}))
```