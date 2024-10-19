### `panic` build in function
- `panic` and `recover` are function-scoped, unlike `try/catch` which is block-scoped. This means you can only recover from a panic withing the same function using a deferred function.
- only for truly exceptional, unrecoverable situations, not for regular error handling. Errors are expected to be handled explicitly by returning them from functions.
- Error handling in Go is more verbose, as you need to explicitly check for errors after every operation. This verbosity is intentional to encourage better error handling practices.
- Propagation : when a `panic` occurs, it unwinds the stack, running deferred function until it reaches the top-level, unlike exception which can be caught at any level.
- `panic/recover` are generally faster than exception because they don't carry the full stack trace.
### function method syntax
```go
func (s *userService) RegisterUser(user *models.User) error { }
```

- `(s *userService)` this is called the receiver. It specifies that this function is a method of the `userService` struct.
- the `s` is like `this` or `self` in other languages, allowing to access the struct's fields and methods