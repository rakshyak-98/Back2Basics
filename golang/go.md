```txt
unused write to field 
```
	- it is a compiler warning that happens when you assign a value to a struct field but never actually use it. 

### How to print value instead of memory address?
When printing struct pointers, `fmt.Println` may print memory addresses instead of values.
```go
package main

import "fmt"

type Type struct {
	Value int
}

func main(){
	t := &Tree({Value: 10} // Pointer to struct
	fmt.Print(*t) // Dereference to point struct fields
}

```

Using `fmt.Prinf` with `%+v`
```go
fmt.Printf("%+v\n", t)
```
