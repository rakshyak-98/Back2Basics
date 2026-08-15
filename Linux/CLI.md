[[Commands]] [[Linux terminal]] [[bash script]] [[login shell]] [[Scripting]] [[Error status code]]

# CLI

> The command-line interface is the primary operator surface on Linux — a text shell reads your line, runs programs, and wires their input and output through pipes.

## Interview Relevance
Nearly every Linux interview starts at the CLI: pipes, redirection, exit status, and when to use shell vs a GUI or API. Interviewers watch for composure with `$?`, quoting, and debugging “command not found.”

## Sources
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/) — deep-dive
- `man 1 bash`, `man 1 intro` — overview

## Core Definition
A **command-line interface** (CLI) exposes the OS through a **shell** (often Bash) that parses a line into a program, arguments, and redirections. Unlike menus, it is scriptable, composable, and works over [[SSH]].

## Key Concepts
- **stdin / stdout / stderr:** File descriptors 0, 1, 2 every process inherits.
- **Exit status:** 0 = success; non-zero = failure — [[Error status code]].
- **Pipes:** Connect one command’s stdout to the next’s stdin.
- **Redirection:** `>`, `>>`, `<`, `2>&1` send streams to files or other descriptors.
- **Expansion:** Shell expands `$VAR`, globs, and quotes before exec.

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

## Real-World Applications
On-call filters production logs over SSH with `journalctl | grep`, pipes into `awk`/`jq`, and gates deploys on non-zero exit codes in CI.

## Pros/Cons or Trade-offs
- **Pro:** Repeatable, remote-friendly, composable — the language of automation.
- **Con:** Easy to shoot yourself with unquoted variables, destructive redirections, or silent pipeline failures without `pipefail`.

## Comparison
vs GUI: CLI wins for scripts, remote access, and log surgery; GUI wins for spatial layout and previews. vs [[Commands]]: CLI is the interaction model; Commands routes to specific binaries. vs [[Linux terminal]]: terminal/PTY is the display path; the CLI is the shell language on top.

## Mistakes to Avoid
- Treating exit code 0 from a pipeline as “all stages succeeded” without `set -o pipefail`.
- Unquoted `$var` that breaks on spaces or glob characters.
- Preferring interactive menus for work that must run the same way in CI tomorrow.
