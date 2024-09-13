- A relocatable schema is a database schema design that allows the schema objects (tables, views, stored procedures, etc.) to be moved or relocated to a different database or schema without affecting the application code that uses those object.
#### Languages typically use relocatable code
##### compile languages
- languages like c, c++, Rust etc. that are compiled to native machine code often use relocatable code.
- the compiler generates object files that contain relocatable code, which is then linked together by a linker to produce the final executable. This allows the code to be loaded and executed at different memory locations.
##### Interpreted languages
- languages like python, Ruby, Perl etc. that are interpreted rather than compiled do not use relocatable code. The interpreter reads and executes the source code directly without generating machine code.
##### Bytecode-compiled languages
- languages like Java, c#, and python (when using JIT compiler) are first compiled to an intermediate bytecode representation. This bytecode is then executed by a virtual machine or JIT compiler. The bytecode itself is not relocatable, but the virtual machine can be designed to support loading and executing the bytecode at different memory location.