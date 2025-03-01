- prototype property points to constructor property of the function you create and not to the build-in `Object()`.
- A *prototype* is an object and every function you create automatically gets a prototype property.
- prototype-based inheritance, objects can inherit properties and methods from other objects.
> [!NOTE] Prototype is an object (not a class or anything special) and every function has a prototype property.

### The difference between `prototype` and `__proto__`

| Feature            | `prototype`                                                          | `__proto__`                                                                      |
| ------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| What it belongs to | A function (constructor function or class)                           | An object (instance of a constructor)                                            |
| Purpose            | The blueprint that instance inherit from                             | A reference to the object's prototype (inherited from constructor's `prototype`) |
| Type               | A prototype of constructor functions                                 | A property of objects                                                            |
| Usage              | Defines what will be inherited by instances                          | Points to the prototype object from which the object inherits                    |
| Accessed on        | Constructor function (`function Foo() {}`)                           | Any JavaScript object `obj.__proto__`                                            |
| Relationship       | `constructorFunction.prototype` becomes the `__proto__` of instances | `obj.__proto__ === Constructor.prototype`                                        |
