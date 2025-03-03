### Primitive values (Stored in Stack)
- Simple data types like integers, floats, characters, booleans, and some immutable types like `null` `undefined`
- Stored directly in the stack memory.
- Access speed -> because the stack is small and operates in a Last-In-First-Out (LIFO) manner.
- Copying Behavior -> when assigned to another variable, a copy of the value is made.

### Non-Primitive values (Stored in Heap)
- Complete data types like arrays, objects, structs, and dynamic data structures (liked lists, trees).
- Memory Storage -> stored in the heap memory, and a reference (or pointer) to the location is stored in the stack.
- Access speed -> Slightly slower than stack access, because heap allocation involves dynamic memory management.
- Copying behavior -> when assigned to another variable, only the reference (memory address) is copied, not the actual object.

