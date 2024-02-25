== 
- equality operator
- converts both operands to a common type before comparing.
===
- strict equality operator
- without type coercion.
- compares both the value and the type of the operands.
## Event Loops
- crucial part of JavaScript concurrency model.
- handle asynchronous operations and callbacks.
### Closures
- is created when a function is defined within another function.
- inner function have access to the outer function's variables, parameters, and even the outer function scope chain.
- even after the outer function has returned, the inner function retains access to the variables in the outer function's scope, as long as the inner function itself is still referenced.
### Prototype-based inheritance
- each object in JavaScript has a prototype object, which it inherits properties and methods from.
### Object
- create with new keyword with constructor function.
	- define function and then using the `new` keyword to create instance of objects based on that constructor.
- Object.create
	- creates a new object with the specified prototype object.
	- allows to create an object that inherits properties from another object directly, without need of constructor function.
- object literals `{}` or ES6 `class` syntax
### Hoisting
- function declarations are moved to the top of their containing scope.
- declarations are hoisted not initialisation or assignments.
### Asynchronous programming
- allows you to performs tasks without blocking the main thread.
- handling operations like fetching data from a server, reading files, or waiting for user input.
- callbacks
	- pass function to be executed once the asynchronous task is complete.
	- can lead to callback hell, making the code difficult to read and maintain.
- promises 
	- cleaner and more flexible way to handle asynchronous operations.
	- promise represents a value (completion or failure).
	- support chaining, error propagation, and composing asynchronous operations.
- async and await
	- `await` keyword provide syntactic sugar for working with promises.
	- `await` keyword pauses the execution of an async function until a promise is settled.
	- this make it more like synchronous code, improving readability and maintainability.
### Techniques for handling errors in JavaScript
- returning rejected promises in asynchronous functions or using `catch` methods to handle asynchronous errors.
- try-catch
	- 
### Event delegation
- attaching an event listener to a parent element to listen for events that occur on its descendant elements.
- allows to handle events centrally, even for dynamically added or removed elements, instead of attaching event listeners to each individual element.