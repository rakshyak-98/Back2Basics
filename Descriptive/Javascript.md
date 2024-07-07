 ## Modules

modules are reusable blocks of code that can be imported into other files.

- used to encapsulate related code into a single unit of code that can be used in other parts of the program.
- split our code into multiple files and reuse it across multiple files.

## how does JavaScript handle errors

### `try...catch` blocks

- basic way to handle errors
- are synchronous and can only be used to handle errors in synchronous code.
- not suitable for asynchronous code, such as callback and promises.

### callback

- callback are most common way to handle errors in asynchronous code.

### Promise

- promises are a more modern way to handle errors in asynchronous code.
    - returned by function and can be chained together.
    - resolved when the function completes and rejected when it fails.

### Event emitter

- event emitters more advanced way to handle errors in asynchronous code.
    - returned by functions and emit an error when they fail.
    - resolved when the function completes and rejected when it fails.

==

- equality operator
- converts both operands to a common type before comparing.

===

- strict equality operator
- without type coercion.
- compares both the value and the type of the operands.

## Event Loops

- JavaScript concurrency model.
- handle asynchronous operations and callbacks.

### Closures

- a function is defined within another function.
- inner function have access to the outer function lexical scope.
- even after the outer function has returned, the inner function retains access to the outer function lexical scope, as long as the inner function itself is still referenced.

### Prototype-based inheritance

- each object in JavaScript has a prototype object,
- which it inherits properties and methods from.

### Object

- create with new keyword with constructor function.
    - create instance of objects based on that constructor.
- Object.create
    - creates a new object with the specified prototype object.
    - allows to create an object that inherits properties from another object directly, without need of constructor function.
- object literals `{}` or ES6 `class` syntax

## weak map

- additional storage of data for objects which are store or managed at another place.
- the main area of application is an addition data storage.
- keys must be objects, not primitive value.
- does not support iteration and methods `keys` `values` `entries`.
- absence of iterations, and the inability to get all current content.

### why such limitation?

- for technical reasons, the current element count of a `WeakMap` is not known. The engine may have cleared it up or not, or did it partially. For that reason, methods that access all keys or values are not supported.

usually, properties of an object or elements of an array or another data structure are considered reachable and kept in memory while that data structure is in memory.

For instance, if we put an object into an array, then while the array is alive, the object will be alive as well, even if there are no other references to it.

```jsx
let john = {name: "John"};
let array = [john];

john = null; // overwrite the reference

// the object previously referenced by john is stored inside the array
// therefore it won't be garbage-collected
// we can get it as array[0]
```

```jsx
let john = {name: "John"};
let array = [john];
john = null; // overwrite the reference

// john is stored inside the map,
// we can get it by using map.keys();
```

weak map is fundamentally different in this aspect.

- keys must be objects, not primitive values.

```jsx
let weakMap = new WeakMap();
let obj = {};
weakMap.set(obj, "ok"); // works fine

// can't use a string as the key
weakMap.set("test", "Wrong"); // Error
```

```jsx
let john = {name: "john"};
let weakMap = new WeakMap();
weakMap.set(john, "...");
john = null; // overwrite the reference
// john is removed from memory;
```

### Hoisting

- function declarations are moved to the top of their containing scope.
- declarations are hoisted not initialization or assignments.

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

### Event delegation

- attaching an event listener to a parent element to listen for events that occur on its descendant elements.
- allows to handle events centrally, even for dynamically added or removed elements, instead of attaching event listeners to each individual element.

## Stream

Streams are objects that allow you to read data from a source or write data to a destination in continuous manner.

- used to handle large amounts of data efficiently.

## de-bouncing

## throttling

## memorize