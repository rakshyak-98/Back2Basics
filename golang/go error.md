[[golang]]

# go error

> go error — panic: runtime error: invalid memory address or nil pointer dereference

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```txt
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x18 pc=0x47a79c]
goroutine 1 [running]:
main.main()
	/home/mihir/GitHub/Practice/lab/go-lang/main.go:14 +0x1c
exit status 2
```
- This means you program tried to call a method or access memory through a `nil` reference.

## Standard config / commands

…

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
