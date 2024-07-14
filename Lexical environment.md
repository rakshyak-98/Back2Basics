- describe how things work. We can't get this object in our code and manipulate it directly.
- Lexical environment consists of two parts
	- Environment Record an object that stores all local variables as its properties (and other information like value of `this`).
	- a reference to the outer _lexical environment_.
> [!INFO] A __variable__ is just a property of the special internal object _Environment Record_. To get or change a variable means to get or change a property of that object.