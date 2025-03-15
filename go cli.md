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

#### Using `pmap` (Memory Map of the Process)
- run your go program and capture its memory map

```shell
go run mian.go & pmap -x $! > memory_snapshot.txt;
```

### Using `/proc` Fielsystem (Detailed Memory Stats)
```shell
go run main.go & cat /proc$!/status | grep Vm > memory_snapshot.txt;
```
- Extracts virtual memory (Vm) statistics of the Go process.

```shell
cat /proc/$!/smaps > memory_snapshot.txt
```

```txt
0000000000400000   6032K r-x-- go
00000000009e4000   5724K r---- go
0000000000f7b000    320K rw--- go
0000000000fcb000    176K rw---   [ anon ]
000000c000000000   4096K rw---   [ anon ]
000000c000400000  61440K -----   [ anon ]
000075289d3c0000    256K rw---   [ anon ]
000075289d400000  32768K rw---   [ anon ]
000075289f400000 263680K -----   [ anon ]
00007528af580000      4K rw---   [ anon ]
00007528af581000 524284K -----   [ anon ]
00007528cf580000      4K rw---   [ anon ]
00007528cf581000 293564K -----   [ anon ]
00007528e1430000      4K rw---   [ anon ]
00007528e1431000  36692K -----   [ anon ]
00007528e3806000      4K rw---   [ anon ]
00007528e3807000   4068K -----   [ anon ]
00007528e3c07000     16K rw-s- go@go1.23.2-go1.23.2-linux-amd64-2025-03-15.v1.count
00007528e3c0b000    640K rw---   [ anon ]
00007528e3cab000   1024K rw---   [ anon ]
00007528e3dab000     68K rw---   [ anon ]
00007528e3dbc000    512K -----   [ anon ]
00007528e3e3c000      4K rw---   [ anon ]
00007528e3e3d000    508K -----   [ anon ]
00007528e3ebc000    384K rw---   [ anon ]
00007528e3f1c000     16K r----   [ anon ]
00007528e3f20000      8K r-x--   [ anon ]
00007ffd256c4000    132K rw---   [ stack ]
ffffffffff600000      4K --x--   [ anon ]
 total          1236432K

```
