`package main` tells the Go compiler: "The package is the entry point of an executable program". Without this Go treats the code as a reusable library/package.

`go mod init example.com/myapp` -> it is a globally unique identifier for you go project. Identify your module uniquely. Without a unique path collision occurs

```txt
github.com/alice/utils
github.com/bib/utils

```
- Go resolves imports relative to the module path.

> [!WARNING]
> every `.go` file must declare a package, and all `.go` files in the same directory (except tests) must belong to the same package.

```txt
project/
├── main.go         -> package main
├── user/
│   ├── user.go     -> package user
│   └── helper.go   -> package user
└── auth/
    └── auth.go     -> package auth
```
- but Go does __not require the package name to match the folder name__

**Why does go do this?**
```txt
go build

↓

read directory

↓

group files by package

↓

compile each package separately

↓

link packages together
```
- the directory is the compilation unit.

```txt
Filesystem path
/home/sde/projects/myapp

        ↓

Module path (global identity)
github.com/sde/myapp

        ↓

Import path
github.com/sde/myapp/internal/auth

```

---

> [!WARNING]
> - go doesn't have enum, so the compiler does not automatically enforce allowed values.
> - The Go designers intentionally avoided adding features that introduce extra complexity. Enum were considered syntactic sugar, because Go can already achieve most enum use cases with (type + const).

They preferred
```txt
type Role string

const (
	Admin   Role = "admin"
	Manager Role = "manager"
	Guest   Role = "guest"
)
```

---

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

> [!INFO] files at the same level cannot be part of different packages within the same directory.
> - all files in a directory must belong the same package.
- if you have `main.go` in a directory, any other file in the same directory must use `package main`.