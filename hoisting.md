**hoisting** means that **variable and function declarations are moved to the top of the code** before it runs. This lets you use them before they are actually written in the code.

JavaScript enables  you to have multiple var statements anywhere in a function
- variable act as they were declared at the top of there containing scope during the compile phase.
- these make possible usage of variable and function before they are declared.
- only variable declaration is hoisted not initialization.
- `const` it is not accurate to say that `const` does not allow hoisting; rather it behaves differently than `var` and `let` due to its initialization requirement and the presence of the temporal dead zone.

> [!NOTE] in case of `const` behavior is slightly different, the declaration of a `const` variable is hoisted to the top of its block scope. However `const` variable must be initialized at the time of declaration. if you try to access a `const` variable before its declaration, it will result in `ReferenceError`.