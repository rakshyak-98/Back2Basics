- A go-routine is a lightweight, concurrent thread of execution in Go.
	- go-routines are much lighter than operating system threads. They use very little memory (typically 2KB per go-routine)
- Managed by go runtime and are cheaper in terms of memory and resources allocation compared to threads in other programming languages.

## How Go-routines work
1. create a go-routine by using `go` keyword followed by a function call. This create a new concurrent task running alongside the current go-routine.