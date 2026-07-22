[[Linux network commands]] [[awk]] [[Find command]] [[journalctl]]

# grep

> One-line: stream filter for lines matching a pattern — first tool for log triage, config audits, and "does this string exist anywhere?" **Kernighan & Pike, Unix philosophy**.

## Mental model

`grep` reads input line-by-line, tests each line against a **regex** (basic by default; extended with `-E`), prints matches. It does not understand structure (JSON, CSV) — pair with `jq`, `awk`, or structured tools when you need fields.

```
file / pipe ──► grep PATTERN ──► matching lines ──► wc / head / xargs
                     │
                     └── exit 0 if match found, 1 if none (scriptable)
```

| Flag family | Purpose |
|-------------|---------|
| `-i` | Case-insensitive |
| `-r` / `-R` | Recursive directory search |
| `-E` | Extended regex (`+`, `\|`, `()`) |
| `-F` | Fixed string (no regex — faster, safer for literals) |
| `-v` | Invert — lines that **don't** match |
| `-c` | Count matches per file |
| `-l` | Filenames only (which files contain it?) |
| `-n` | Line numbers |
| `-A/-B/-C` | Context lines after/before/around match |

## Standard config / commands

```bash
# Baseline log triage
grep -i error /var/log/syslog
journalctl -u nginx --no-pager | grep -E 'error|crit|emerg'

# Recursive config audit — skip binaries
grep -rn 'PasswordAuthentication' /etc/ssh/
grep -r --include='*.conf' 'listen' /etc/nginx/

# Context: show line + next line (stack traces, multi-line errors)
grep -A2 -B1 'Exception' app.log

# Fixed string when pattern has regex metacharacters
grep -F '$HOME' script.sh          # literal $HOME, not end-of-line

# Which files mention the secret?
grep -rl 'API_KEY' /opt/app/config/

# Pipeline: find PIDs listening on port from ss output
ss -lntp | grep ':443'

# Count occurrences per file
grep -c 'FAILED' /var/log/auth.log

# Invert: lines without the noise
grep -v '^#' /etc/app.conf | grep -v '^$'   # strip comments + blanks
```

**Extended regex examples (`-E`):**

```bash
grep -E 'error|warn|fatal' app.log
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' access.log   # ISO dates
grep -E 'timeout|refused|reset' /var/log/syslog
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `grep` hangs on huge file | `grep --line-buffered` or `tail -f \| grep` | Don't grep entire multi-GB logs — use [[journalctl]] time bounds or `zgrep` on rotated `.gz` |
| No matches but you know string exists | Wrong case (`-i`), wrong file encoding, binary file | `grep -a` for text-in-binary; `file` the target; try `strings` |
| Regex matches too much | Unescaped `.` `*` `(` | Use `-F` for literals; test with `grep -E --color=always` |
| `grep -r` searches `.git`, `node_modules` | `--exclude-dir` | `grep -r --exclude-dir={.git,node_modules} PATTERN .` |
| Permission denied mid-recurse | Normal on `/etc`, `/var` | Run with `sudo` or narrow path; use `-s` to silence errors |
| Pipeline exits 1 in script | grep found nothing | `grep -q` for boolean test; `\|\| true` only when you mean it |

## Gotchas

> [!WARNING]
> **Default regex is basic** — `+`, `|`, `()` need `-E`. A pattern like `error|warn` without `-E` matches literal `error|warn`.

> [!WARNING]
> **`grep` on directories without `-r` prints "Is a directory"** — always `-r` for trees, or `grep PATTERN /path/to/file`.

> [!WARNING]
> **Binary files** — grep may print "Binary file matches" and skip. Use `-a` to treat as text, or `strings` / `rg` (ripgrep) for codebases.

> [!WARNING]
> **Exit code 1 = no match** — not an error. Scripts using `set -e` with `grep` in a pipeline need `grep -q PATTERN \|\| [[ $? -eq 1 ]]` or `if grep -q …`.

## When NOT to use

- **Structured data** (JSON, YAML keys) → `jq`, `yq`, not grep.
- **Column extraction** → [[awk]] or `cut`.
- **Large codebases** → `rg` (ripgrep) — respects `.gitignore`, faster, better defaults.
- **Live follow** → `tail -f \| grep` or [[journalctl]] `-f`, not re-running grep in a loop.

## Related

[[awk]] [[Find command]] [[journalctl]] [[Linux network commands]] [[bash script]]
