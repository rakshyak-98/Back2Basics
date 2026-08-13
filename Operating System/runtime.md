[[Operating System]] [[Runtime Environment]] [[interpreter]] [[OS program]] [[Heap memory]]

# Runtime

> Runtime is the active phase when a program executes — and colloquially the libraries and services that phase depends on, distinct from compile/link time.

**Compile time:** source → objects ([[linker]]). **Runtime:** CPU executes instructions, allocator serves [[Heap memory]], I/O uses [[file descriptors]].

Managed languages add bytecode execution ([[interpreter]]), JIT compilation, and garbage collection inside the [[Runtime Environment]].

Debugging “runtime error” versus “compile error” separates logic after launch from syntax and type failures before launch.

## Sources

- Wikipedia: [Runtime system](https://en.wikipedia.org/wiki/Runtime_system)
- Bryant & O’Hallaron, *Computer Systems*
