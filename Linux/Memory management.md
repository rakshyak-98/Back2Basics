## How does the stack memory usage differ between single-thread and multi-threaded processes

### Stack memory in Single-Threaded Processes

##### Dedicated stack
- A single-threaded process has a dedicated stack that is allocated when the process starts. This stack is used for function calls, local variables, and return addresses.
- The size of the stack is typically fixed and determined at the start of the program, which can lead to stack overflow if the stack size limit is exceeded due to deep recursion or excessive local variable allocation.
```bash
ulimit -a; # check all current resource limit.
cat /proc/<pid>/limits; # to check limit of a process.
```

##### Isolation
- the stack is isolated from other processes and threads, meaning that any stack corruption or overflow will only affect that specific process.

##### Performance
- stack operations (push and pop) are generally faster due to the LIFO nature of stack management and the fact that memory allocation is handled automatically by the compiler.

### Stack memory in Multi-Threaded Processes
##### Multiple stack
- Each thread within a multi-threaded process hash its own stack. This allows threads to maintain their own execution context, including local variables and function calls.
- The kernel allocates a separate stack for each thread when it is created, which can lead to increased memory usage compared to a single-threaded process.

##### Shared Memory Space
- while each thread has its own stack, all thread within the same process share the same heap and global variables. This sharing can lead to potential issues such as race conditions if not managed properly.
- The shared memory space allows for more efficient communication between threads, as they can directly access shared variables without the need for [[Inter Process Communication]] mechanisms. 

##### Stack size Management
- the stack size for threads can often be configured when the thread is created. This flexibility allows developers to optimize stack usage based on the expected depth of function calls and local variable requirements.
- however since threads share the same process memory, a stack overflow in one thread can potentially affect the entire process, leading to crashes or undefined behavior.

##### Overhead
- multi threaded processes generally have lower overhead for context switching compared to multi-process systems, as threads within the same process share the same memory space. However, the management of multiple stacks can add complexity.