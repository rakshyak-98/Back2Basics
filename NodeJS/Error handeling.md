```js
try{
	...
}catch(error){
	console.log(error.name);
}
```

## Creating Custom Error

create errors with a custom name is to extend the built-in `Error` class using ES6 class syntax

```js
class ValidationError extends Error {
	constructor(message){
		super(message);
		this.name = "ValidationError"
		// Optional: clean up stack trace (hides internal constructor calls)
		Error.captureStackTrace(this, this.constructor);
	}
}

class NotFoundError extens Error {
	constructor(message = 'Resource Not Found'){
		super(message);
		this.name = this.constructor.name;
		Error.captureStackTrace(this, this.constructor);
	}
}

class UnauthorizedError extends Error {
	constructor(message = "Unauthorized") {
		super(message);
		this.name = this.constructor.name;
		this.statusCode = 401;
		Error.captureStackTrace(this. this.contructor);
	}
}


```

> [!NOTE]
> `ReferenceError: Must call super constructor in derived class before accessing 'this' or returning from derived constructor`
> - this comes when you access `this.constructor.name` before calling `super(message)`

```js
class AppError extens Error {
	constructor(statusCode, message, isOperational = true){
		super(message); // 
		this.name = this.constructor.name;
		this.statusCode = stausCode;
		this.isOperational = isOperational;
		Error.captureStackTrace(this, this.constructor);
	}
}

class BadRequestError extends AppError {
	constructor(message= "Bad Request"){
		super(400, message);
	}
}

class ForbiddenError extends AppError {
	constructor(message = "Forbidden" ){
		super(403, message);
	}
}

```