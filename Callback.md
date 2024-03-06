define an event handler for the user action events, this accepts a function, which will be called when the event is triggered.
- callback add a level of nesting (code get complicated to Humans).
- ES6 features use Promises and Async/Await.
- simple function passed as a value to another function.
- only executed when the event happens.
We can do this because JavaScript has first-class functions, which can be assigned to variables and passed around to other functions (called [[higher-order functions]]).
> [!Note] common to wrap all client code in a `load` [[event listener]] on the `window` object.
```javascript
window.addEventListener('load', () => {
	// window loaded
	// do what you want
})
```

- used in [[DOM]] events, [[XHR request]], timers
### How do you handle errors with Callbacks?
- very common strategy is to use NodeJS adopted: the first parameter in any callback function is the error object. If their is no error the object is null.