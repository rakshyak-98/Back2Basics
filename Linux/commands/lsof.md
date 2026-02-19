```bash
lsof -i :<port>; # if you know the port
pgrep -f "<command>"; # if you know the command
pgrep -f "npm run dev"; # if you know the command
```

- List St Open Files -> shows all open files on the system and which process have them open.

> [!INFO]
> In linux "Everything is a file". In Linux (and Unix-like systems), almost everything the kernel deals with is represented as a file (or file like object)

- Regular files on disk (`/etc/passwd`, logs, images…)
- Directories
- Devices (`/dev/sda`, `/dev/null`, `/dev/tty`)
- Pipes (named & anonymous)
- Sockets (network connections — TCP, UDP, UNIX domain sockets)
- Memory-mapped files
- Executable code (the binary itself while running)
- Standard streams (stdin=0, stdout=1, stderr=2 of every process)

open file ->  