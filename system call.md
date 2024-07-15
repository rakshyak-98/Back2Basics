- these functions allow user programs to request services from the kernel, such as file operations, process control, and communication between processes.
- low level functions
- primary way for a program to interact with the operating system.
- __System call Table__ the Linux kernel uses a system call table where each entry is a pointer to a system call handler.
	- when a _system call_ is made, the kernel uses the system call number to look up the corresponding function pointer and execute the appropriate handler.

> [!INFO] When a program needs to request a service from the operating system's kernel, such as reading from a file, writing to a file, creating a new process,or communicating with hardware devices, it makes a system call.

> [!INFO] User programs operate in user mode.

### Computed calls
- process where the address of the function to be called is determined at runtime rather than at compile time.
#### how computed calls work
- __Function Pointer__ holds the address of a function.
	- the function to be called can be changed at runtime by assigning a different function's address to the pointer.
	- the function pointer is then used to call the function. Since the actual function being called can change, this provides flexibility and dynamism in program behavior.
- computed calls are crucial for implementing _polymorphism_ is __C language__.
	- _Structures_ can contain function pointers, allowing different structures to have different implementations of the same operations.