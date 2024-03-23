- tasks are handled sequentially within the same thread.
- JavaScript is synchronous by default and is single threaded within the same process.
- all tasks and operations and handled sequentially within that single thread.
- means code cannot create new threads and run in parallel.
- used to handle work that  will result in visual changes to the user interface.
- data can change constantly.
	- it would be extremely slow if the JavaScript engine had to check each time which data type a certain value has.
	- it can happen that the same piece of code suddenly returns a different type of data. If that happens machine code gets de-optimized, and the engine falls back to interpreting the generated byte code.