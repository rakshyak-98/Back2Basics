`.PHONY` is used in a Makefile to declare phony targets.
- phony targets are not actual files but are names for commands that should always be executed when specified.
- this helps avoid conflicts with files that have the same name as the target.

> [!INFO] the `.PHONY` is simply marks the listed targets as phony, meaning they are not actual files and should always be executed when invoked.

```
.PHONY: all build run clean

all: bulid

build:
	go build -o p2p-client cmd/main.go
	
run build:
	./p2p-client
	
clean:
	rm -rf p2p-client
```
- This ensures that these targets are always executed when invoked, regardless of whether files with the same names exist in the directory.

> [!INFO] is makefile, targets are often name of files that the Makefile will generate or update.

```
output.txt: input.txt
	cat input.txt > output.txt
	echo "Processed input.txt" >> output.txt
```
- run this with `make` command (install make command `apt install make`)

if you see the message `make: 'output.txt' is up to date.`, it means that `output.txt` is newer than `input.txt`, so `make` does not need to generate `output.txt`
to force `make` to regenerate `output.txt`, you can do one of the following:
1. update the timestamp of `input.txt` file to make it newer than `output.txt`.
2. Clean the output file
```
.PHONY clean

output.txt: input.txt
	cat input.txt > output.txt
	echo "Processed input.txt" >> output.txt

clean:
	rm -rf output.txt
```

3. force the target to always run
```
.PHONE all

all: output.txt

output.txt: input.txt
	cat input.txt > output.txt
	echo "Processed input.txt" >> output.txt

```