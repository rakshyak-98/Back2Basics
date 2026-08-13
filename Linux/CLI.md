[[Commands]] [[Linux terminal]] [[bash script]] [[login shell]]

# CLI

> The command-line interface is the primary operator surface on Linux — a text shell reads your line, runs programs, and wires their input and output through pipes.

A **command-line interface** (CLI) exposes the operating system through a **shell** (usually Bash on interactive systems) that parses lines into a program name, arguments, and redirections. Unlike graphical menus, the CLI is scriptable, composable, and works over [[SSH]].

## How a command runs

```
you type:  grep error /var/log/syslog | wc -l
              │
              ▼
shell parses words, expands $VAR and globs
              │
              ▼
grep runs ──stdout──► pipe ──► wc runs ──► prints count
```

| Piece | Role |
|-------|------|
| **stdin / stdout / stderr** | Standard streams every process inherits (file descriptors 0, 1, 2) |
| **exit status** | 0 = success; non-zero signals failure — see [[Error status code]] |
| **pipes** | Connect stdout of one command to stdin of the next |
| **redirection** | `>`, `>>`, `<`, `2>&1` send streams to files or other descriptors |

## Everyday patterns

```bash
# Help and manual
man grep
grep --help

# Run with elevated privileges when the task requires it
sudo systemctl restart nginx

# Chain on success / failure
test -f /etc/hosts && echo "exists" || echo "missing"

# Capture output
output=$(hostname -f)
```

## Choosing CLI vs GUI

Use the CLI when you need repeatability (scripts), remote access ([[SSH]]), log filtering ([[grep]], [[journalctl]]), or automation in CI. Use a desktop GUI when spatial layout or rich previews matter more than piping.

## Debugging a stuck or silent command

| Symptom | Check |
|---------|-------|
| Hangs with no output | `strace -p PID` or `lsof -p PID` — waiting on network or lock? |
| "Command not found" | `echo $PATH`; `type -a cmd`; package installed? |
| Permission denied | `ls -l` on target; need `sudo` or different user? |
| Wrong result in script | Quote variables: `"$var"`; see [[Bash syntax]] |

## Related

[[Commands]] · [[Linux terminal]] · [[login shell]] · [[Scripting]] · [[bash script]]

## Sources

- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/)
- `man 1 bash`, `man 1 intro`
