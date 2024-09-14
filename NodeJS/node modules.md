Node.js does not use traditional linkers like those found in compiled languages (e.g C or C++) due to its architecture and the nature of JavaScript an an interpreted language.
#### Dynamic Module loading
- employs a *dynamic module loading system* through the `require()` function, which allows modules to be loaded at *runtime*.
- Node.js allows modules to loaded dynamically  at runtime using the `require()` function. This means that modules are not all loaded upfront; instead, they are loaded as needed, which can lead to more efficient memory usage and faster startup time.
### CommonJS Module System
- Node.js uses the CommonJS module system, which is designed to work seamlessly with JavaScript's *asynchronous* and *event-driven* nature. In this system, each file is treated as a separate module, and the `exports` and `require` objects facilitate the sharing of functionality between them.
- this functionality eliminates the need for a linker since module dependencies are resolved at runtime rather than at compile time.