
## How process memory spaces work in Linux (modern x86-64)

> [!INFO]
> Every process in Linux gets its own virtual address space. An illusion of having almost the entire memory for itself.
> Process sees only virtual addresses.


```bash
cat /proc/<pid>/maps          # memory regions + permissions
pmap -XX <pid>                # more human readable
gdb -p <pid> → (gdb) info proc mappings
```

## Find which user own the process

```bash
ps -p <pid-from-pm2> -o user; # Definitive answer
```

## Process

```bash
nsenter -t <pid> -m -u -i -n -p /bin/bash
```
- pts - pseudo terminal slave.
 -tty - teletypewriter.
- pts - first terminal pseudo terminal slave window. A pair of virtual terminal devices that allow a terminal emulator gnome-terminal to communicate with a program as if it were a terminal.
- The master end of a pseudo terminal is connected to the terminal emulator, where a slave end is connected to the program. The slave end is identified by a device name that begins with `pts/` followed by a number that identifies the specific pseudo terminal.

> `pts` notation is specified to Unix-like systems, and may not be used on other operating systems.

- SPID - system process id. Identify the process internally. Used to track the process across different terminal sessions.

- STAT - stands for status.
- D - Uninterruptible sleep (usually input or output).
- R - running or run-able
- S - interruptible sleep (waiting for an event to complete)
- T - stopped, either by a job control signal or because it is being traced.
- Z - defunct (zombie) process, terminated but not reaped by its parent.
`tty` column - display the terminal device associated with a process.

### sha bang

directive meaning - an official or authoritative instruction.

- involving the management or guidance of operations.

shebang is the character sequence consisting of the characters `#!` when a text file with a shebang is used as if it is an executable in a Unix operating system, the program loader mechanism parses the rest of the file’s initial line as an interpreter directive. The loader executes the specified interpreter program, parsing to it as an argument using the path that was initially used when attempting to run the script, so that the program may use the file as input data.

### kill process

`pgrep -l -u $USER` list the process and get the process id, user `kill` command to kill the process.

```bash
kill -l; # list all the signal names;
sudo lsof -i -P -n | grep LISTEN
kill -s QUIT [process id]
```

### kill a process by name not pid

`pkill [process name]`
