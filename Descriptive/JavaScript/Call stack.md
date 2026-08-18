- When a function runs, it is pushed onto the call stack.
- The call stack lives inside the JavaScript engine.
- When a function returns, it is popped off the stack.

**Why it exists:**
- Track which function should get control back when the current one finishes.
- An active function is one that was called but has not returned yet.

> [!INFO] Adding frames is called *winding*; removing them is *unwinding*.

Details depend on the compiler, OS, and CPU instruction set.

## Structure

The call stack is made of [[stack frame]] entries (also called activation records or frames).
