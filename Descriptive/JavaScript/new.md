with a constructor function
- it creates a new empty object.
- it sets the `[[prototype]]` of the new object to the `prototype` property of the constructor function.
- it calls the constructor function with `this` set to the newly created object.
- it returns  the newly created object unless the constructor function explicitly returns another object.