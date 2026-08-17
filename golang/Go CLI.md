[[Go CLI]] [[INDEX]]

# golang CLI

> Go toolchain CLI — mod, build, test, and vet.

---

## go CLI

From [[Go CLI]].

```bash
go mod init github.com/you/app
go get example.com/lib@v1.2.3
go mod tidy && go mod verify
go run ./cmd/app
go build -trimpath -ldflags="-s -w" -o bin/app ./cmd/app
go test ./... -count=1
go test -race ./...
go list -m all
go clean -cache
go mod edit -replace example.com/lib=../lib
```

```bash
# memory snapshot while running
go run . & pid=$!; sleep 1; pmap -x $pid | head
grep Vm /proc/$pid/status
```
