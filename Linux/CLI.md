[[Linux terminal]] [[bash script]] [[grep]] [[fzf]] [[Find command]]

# CLI

> One-line: the Linux **command-line interface** — compose small tools via pipes, redirect streams, and automate with shell; the operator's primary debugger. **Kernighan & Pike, POSIX shell**.

## Mental model

Everything is a file descriptor: **stdin (0)**, **stdout (1)**, **stderr (2)**. Programs read stdin, write stdout, errors to stderr. The shell connects them with pipes (`|`), redirects (`>`, `>>`, `2>&1`), and subshells (`$()`, `$()`).

```
Keyboard ──stdin──► command ──stdout──► pipe ──► next command ──► terminal/file
                      │
                      └──stderr──► journal / 2>&1 merge
```

| Concept | Meaning |
|---------|---------|
| Exit code | 0 = success; non-zero = failure (`$?`) |
| Pipe | stdout of left → stdin of right |
| `2>&1` | Merge stderr into stdout |
| `\|` pipeline | Each stage is separate process |
| `$()` | Capture output as string |
| `set -euo pipefail` | Fail fast in scripts ([[bash script]]) |

**Operator workflow:** observe → narrow → act → verify.

```
symptom ──► ss/journalctl/ps ──► grep/awk ──► fix ──► re-check
```

## Standard config / commands

**Navigation & inspection:**

```bash
pwd                          # where am I
ls -la                       # permissions, hidden files
cd -                         # previous directory
less /var/log/syslog         # paginated read; q to quit
tree -L 2 /etc/nginx/        # structure (install tree)
```

**Pipes and redirects:**

```bash
cmd > file                   # overwrite stdout
cmd >> file                  # append
cmd 2>&1 | tee log.txt       # stdout+stderr to pipe and file
cmd &>/dev/null              # discard all output

# Count errors in log
grep -c ERROR app.log

# Top talkers from access log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
```

**Process & system:**

```bash
ps aux | head
top                          # or htop
df -h                        # disk
free -h                      # memory
uptime                       # load averages
```

**Network quick checks:**

```bash
ss -lntp                     # listening ports
curl -I https://example.com  # HTTP headers
ping -c 3 8.8.8.8
```

**Safety habits:**

```bash
# Preview before destroy
rm -i file
find . -name '*.tmp' -print   # print before -delete

# Quote variables
cp "$src" "$dst"

# Script header
set -euo pipefail
IFS=$'\n\t'
```

**Productivity:**

```bash
history | grep ssh           # recall command
!!                           # repeat last
Ctrl+R                         # reverse search ([[fzf]] if configured)
man ss                       # local docs
help cd                      # shell builtins
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Command not found" | `which cmd`; `$PATH` | Install package; fix PATH in profile |
| Permission denied | `ls -l`; `id` | `chmod`/`chown`; run as correct user; not `chmod 777` |
| Pipe silently empty | Left command failed (`set -o pipefail`) | Check `$?` per stage |
| Script works interactively, fails in cron | Env, PATH, cwd | Absolute paths; set vars in script |
| Terminal garbled | `echo $TERM` | `reset`; fix TERM |
| Ctrl+C doesn't stop | Process ignoring SIGINT | `Ctrl+\` (SIGQUIT); kill from another session |

## Gotchas

> [!WARNING]
> **Parsing `ls` output** — filenames with newlines/spaces break. Use `find -print0` + `xargs -0`.

> [!WARNING]
> **`rm -rf` with unquoted `$var`** — if empty, deletes cwd. Always quote; validate non-empty.

> [!WARNING]
> **Running as root by default** — use `sudo` for targeted elevation; prod changes need change control.

> [!WARNING]
> **Copy-paste from web** — smart quotes and em-dashes break shell syntax.

## When NOT to use

- **Heavy data transformation at scale** → Python/awk scripts, DB, dedicated tools.
- **GUI-only tasks** → desktop settings (unless [[gsetting]] / D-Bus).
- **Immutable infra** → config management API, not manual SSH edits (still CLI, different workflow).

## Related

[[Linux terminal]] [[bash script]] [[grep]] [[fzf]] [[Find command]] [[ss]] [[journalctl]] [[Commands]]
