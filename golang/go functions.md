```go
func add(a int, b int) int {
	return a+b;
}

func getDetails() (string, int) {
	// Multiple Return values: Can return multiple values;
	return "Alice", 25
}

func getStatus() (status string, code int) {
	// Named Return Values
	// Return values are named, and you can return them without explicitly using return.
	status = "Success"
	code = 200
	return
}

func sum(nums, ...int) int {
	// Functions that accept a variable number of arguments.
	total := 0
	for _,num := range nums {
		total += num
	}
	return total
}

greet := func(name string) {
	fmt.Println("Hello, ", name)
}
greet("Foo")

func adder(fn func(int, int) int, a, b int) int {
	// first-class functions
	return fn(a, b)
}
result := operate(multiply, 4, 5)

func adder(x int) func(int) int {
	// function returning a function
	return func(y int) int {
		return x + y
	}
}

type Circle struct {
	radius float64
}

func(c *Circle) area() float64 {
	// Method function Functions associated with a type, commonly used for object-oriented programming in go.
	return 3.14 * c.radius * c.radius
}
```

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