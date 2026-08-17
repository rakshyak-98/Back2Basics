[[Commands]] [[Linux terminal]] [[bash script]] [[login shell]] [[Scripting]] [[Error status code]]

# CLI

> The command-line interface is the primary operator surface on Linux — a text shell reads your line, runs programs, and wires their input and output through pipes.

```txt
        CLI ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Nearly every Linux interview starts at the CLI: pipes, redirection, exit stat…

## Sources
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/) — deep-dive
- `man 1 bash`, `man 1 intro` — overview

## Key Concepts
- **stdin / stdout / stderr:** File descriptors 0, 1, 2 every process inherits.
- **Exit status:** 0 = success; non-zero = failure — [[Error status code]].
- **Pipes:** Connect one command’s stdout to the next’s stdin.
- **Redirection:** `>`, `>>`, `<`, `2>&1` send streams to files or other descriptors.
- **Expansion:** Shell expands `$VAR`, globs, and quotes before exec.


- **Core:** A **command-line interface** (CLI) exposes the OS through a **shell** (often …

## Technical Details
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
| **stdin / stdout / stderr** | Standard streams (fds 0, 1, 2) |
| **exit status** | 0 = success; non-zero signals failure |
| **pipes** | stdout of one → stdin of next |
| **redirection** | `>`, `>>`, `<`, `2>&1` |

```bash
man grep
grep --help
sudo systemctl restart nginx
test -f /etc/hosts && echo "exists" || echo "missing"
output=$(hostname -f)
```

| Symptom | Check |
|---------|-------|
| Hangs with no output | `strace -p PID` or `lsof -p PID` |
| "Command not found" | `echo $PATH`; `type -a cmd` |
| Permission denied | `ls -l` on target; need `sudo`? |
| Wrong result in script | Quote `"$var"`; see [[Bash syntax]] |

## Mistakes to Avoid
- **Mistake:** Treating exit code 0 from a pipeline as “all stages succeeded” w…
- **Mistake:** Unquoted `$var` that breaks on spaces or glob characters
- **Mistake:** Preferring interactive menus for work that must run the same way…

## Pros/Cons or Trade-offs
- **Pro:** Repeatable, remote-friendly, composable — the language of automation.
- **Con:** Easy to shoot yourself with unquoted variables, destructive redirections, or silent pipeline failures without `pipefail`.

## Comparison
- vs GUI: CLI wins for scripts, remote access, and log surgery


### Use cases
- On-call filters production logs over SSH with `journalctl | grep`, pipes into…
