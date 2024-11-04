### setup debugger
- prerequisite
	- install Delve debugger for golang
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

```bash
cat go.mod; # check for module: "module github.com/username/myproject"
# project name is myproject
```

> [!NOTE] The `+incompatible` suffix in the version string indicates that the package does not use Go modules and does not have a `go.mod` file in its repository.

- - `+incompatible` suffix to indicate this incompatibility.
- This does not affect the functionality of the package itself; it just serves as a warning that the package may not fully support module semantics.

> [!NOTE] include debugging symbols in the binary. These symbols provide essential information to the debugger about the structure and flow of your code. Without these symbols, the debugger would not be able to provide meaningful insights into the state of your program during execution.

```bash
go build -gcflags="all=-N -l" -o <my-app> 
```
	
```json
{
	"configuration": [
		{
			
		}
	]
}
```

### Debugger
```bash
sudo apt install delve; # install go debugger
```

```bash
break main.main; # break at main function
stack; # stdout the current stack frame
locals; # view current stack frame variables reference
print <variable>; # view the variable ref or value
```

#### Why the `// indirect` tag appears?
- in Go the `// indirect` suffix in `go.mod` means that these dependencies are not directly used in code but are required by other dependencies (often called *transitive dependencies*)