### setup debugger
- prerequisite
	- install Delve debugger for golang
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

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