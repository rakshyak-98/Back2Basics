```shell
go mod init <domain name/username/module name>;
go mod tidy;
go mod verify;
go get <package>;
go run <file.go>;
go build;
go install;
```

```shell
go mod edit --replace example.com/module=../module; # Replace a module with local version
```

```shell
go clean -cache;
go list -m all; # list dependencies
go get -u ./..; # upgrade dependencies
go doc <package>;
```