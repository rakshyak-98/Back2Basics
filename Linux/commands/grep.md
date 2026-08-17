[[Commands]] [[awk]] [[Find command]] [[journalctl]] [[bash script]]

# grep

> grep filters lines matching a pattern — first tool for log triage, config audits, and “does this string exist anywhere?”

```txt
        grep ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Flags matter: `-E` vs `-F`, exit 1 = no match (not error), and when to use ri…

## Sources
- [grep(1)](https://man7.org/linux/man-pages/man1/grep.1.html) — deep-dive
- [GNU grep manual](https://www.gnu.org/software/grep/manual/) — overview

## Key Concepts
- **`-i` / `-v` / `-n` / `-c` / `-l`:** Case, invert, line numbers, count, filenames.
- **`-r` / `-R`:** Recursive trees (with `--exclude-dir`).
- **`-E` vs `-F`:** Extended regex vs fixed string.
- **`-A/-B/-C`:** Context for stack traces.
- **Exit codes:** 1 is “no match” — breaks `set -e` if mishandled.


- **Core:** `grep` reads input line-by-line, tests each line against a regex (basic by de…

## Technical Details
```bash
grep -i error /var/log/syslog
journalctl -u nginx --no-pager | grep -E 'error|crit|emerg'

grep -rn 'PasswordAuthentication' /etc/ssh/
grep -r --include='*.conf' 'listen' /etc/nginx/
grep -A2 -B1 'Exception' app.log
grep -F '$HOME' script.sh
grep -rl 'API_KEY' /opt/app/config/

ss -lntp | grep ':443'
grep -c 'FAILED' /var/log/auth.log
grep -v '^#' /etc/app.conf | grep -v '^$'

grep -E 'error|warn|fatal' app.log
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' access.log
grep -r --exclude-dir={.git,node_modules} PATTERN .
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Hangs on huge file | Scope | Time-bound journal; `zgrep`; don’t grep multi-GB whole |
| No matches but string exists | Case/binary | `-i`; `-a`; `file` the target |
| Regex too greedy | Metacharacters | `-F` for literals |
| `set -e` fails on no match | Exit 1 | `grep -q … \|\| true` only when intentional |

## Mistakes to Avoid
- **Mistake:** Using `error|warn` without `-E` (literal pipe)
- **Mistake:** Grepping binary files without `-a` / proper tools
- **Mistake:** Treating exit 1 as a hard script failure when “no match” is expe…

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous, scriptable, pipeline-friendly.
- **Con:** Poor on structured data; recursive from `/` is an IO storm.
- **Trade-off:** `rg` for codebases (gitignore-aware) vs grep for logs on minimal hosts.

## Comparison
- vs [[awk]]: fields/aggregates


### Use cases
- Finding `PasswordAuthentication` in sshd configs, filtering journal noise, an…
