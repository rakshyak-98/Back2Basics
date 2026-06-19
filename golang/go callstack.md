class stack unwinding -> walking backward through the chain of function calls, exiting one function at a time until reaching the top.

"During each exit, Go runs any `defer` statements"

When `panci()` happens, Go does not immediately destroy a function. Before removing a function from the call stack, Go checks.

"Does this function have any `defer` statements? If yes, execute them first."

```go
panic
↓
for every function being removed from stack:
    run deferred functions
    remove function from stack
```