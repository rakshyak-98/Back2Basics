strict mode
- If the function is called without being accessed on anything, `this` will be `undefined`
non-strict mode
- if a function is called with `this` set to `undefined` `null` , `this` gets substituted with `globalThis`. 
- if the function is called with `this` set to a primitive value, `this` get substituted with the primitive value's wrapper object.
you can  also explicitly set the value of `this` using the
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