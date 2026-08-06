[[golang]]

# go-routines

> One-line: what / why for **go-routines** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#How Go-routines work]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- A go-routine is a lightweight, concurrent thread of execution in Go.
	- go-routines are much lighter than operating system threads. They use very little memory (typically 2KB per go-routine)
- Managed by go runtime and are cheaper in terms of memory and resources allocation compared to threads in other programming languages.

## Standard config / commands

…

## How Go-routines work

1. create a go-routine by using `go` keyword followed by a function call. This create a new concurrent task running alongside the current go-routine.

```go
go func() {
	for event := range events {
		fmt.Printf("received: %v\n", event)
	}
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
