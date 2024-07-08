- The value of `this` is the object the one used to call the method.

> [!NOTE] Only the moment of call matters.
```javascript
function makeUser(){
	return {
		name: "John",
		ref: this
	}
}

let user = makeUser(); // called as a function not method
console.log(user.ref.name); // Error: Cannot read property 'name' ...
```

- the value of `this` is evaluated during the run-time, depending on the context.
- `this` value is evaluated at call-time and does not depend on where the method was declared, but rather on what object.
- _arrow function_ have no `this`. If we reference `this` from such a function, it's taken from the outer "normal" function.
	- a special feature of arrow function, it's useful when we actually do not want to have a separate `this`, but rather to take it from the outer context.
- `this` is not bound unlike most other programming languages. It can be used in any function even if it's not a method of an object.
```javascript
'use strict'
function f(){
	console.log(this); // calling without an object this == undefined
}
```
### strict mode
- If the function is called without being accessed on anything, `this` will be `undefined`
non-strict mode
- if a function is called with `this` set to `undefined` `null` , `this` gets substituted with `globalThis`. 
- if the function is called with `this` set to a primitive value, `this` get substituted with the primitive value's wrapper object.
### you can  also explicitly set the value of `this` using the
- `Function.prototype.call()`
- `Function.prototype.apply()`
- `Reflect.apply()`
- `Function.prototype.bind()` : create a new function with a specific value of `this` that doesn't change regardless of how the function is called.
### Callback
- `this` depends on how the callback is called.
- all iterative array methods and related ones like `Set.prototype.forEach()` accept an optional `thisArgs` parameter.
### Arrow function
- `this` retains the value of the enclosing lexical context's `this`.
- when evaluating an arrow function's body, the language does not create a new `this` binding.
- in global code, `this` is always `globalThis` regardless of strictness, because of the `global context` binding.
- arrow function create a [[closure]] over the `this` value of its surrounding scope.
### Constructors
- its `this` is bound to the new object being constructed, no matter which object the constructor function is accessed on.