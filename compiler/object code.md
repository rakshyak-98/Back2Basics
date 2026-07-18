 is a product of a [[compiler]].
 - sequence of statements or instructions in a computer language.
 - a portion of machine code that has not yet been linked into a complete program.
 - require a [[linker]] to link with other modules.
### Overview
Typically, an object file can contain three kinds of symbols:
- defined "external" symbols, sometimes called "public" or "entry" symbols, which allow to be called by other modules
- undefined "external" symbols, which reference other modules where these symbols are defined.
- local symbols, used internally within the object file to facilitate relocation.

>[!INFO] linker use offset or placeholders in object code to connect everything together.

>[!INFO] where machine code is binary code that can be executed directly by the CPU, object code has the jumps partially parameterized so that a linker can fill them in.