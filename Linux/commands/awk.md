[[Commands]] [[grep]] [[jq]] [[Find command]] [[Scripting]]

# awk

> awk walks a file line by line — match a pattern, run an action on fields.

## Interview Relevance
Classic filter question: `$1`/`NF`/`NR`, `-F`, `BEGIN`/`END` aggregates — and knowing when CSV/JSON needs something else.

## Sources
- [GNU awk User’s Guide](https://www.gnu.org/software/gawk/manual/) — deep-dive
- [awk(1)](https://man7.org/linux/man-pages/man1/awk.1p.html) — overview

## Core Definition
For each record (usually a line), awk splits fields on `FS`, optionally matches a pattern, then runs an action. `BEGIN` runs once first; `END` once last. No pattern means every line; no action means print the match.

## Key Concepts
- **`$0` / `$1`…:** Whole line / fields after split.
- **`NF` / `NR`:** Field count this line / record number; `$NF` is last field.
- **`-F` / `FS`:** Input separator (`-F:` for `/etc/passwd`).
- **`BEGIN` / `END`:** Setup and teardown (sums, headers).
- **Whitespace split:** Collapses runs of spaces; empty columns can disappear.

## Technical Details

```txt
input lines ──► split on FS ──► match pattern? ──► run action ──► next line
```

```bash
awk '{ print $2 }' file.txt
awk '{ print $1, $NF }' file.txt
awk -F: '{ print $1, $7 }' /etc/passwd

awk '/error/ { print }' app.log
awk '$3 > 100 { print $0 }' data.txt

awk '{ sum += $2 } END { print "Total =", sum }' numbers.txt
awk 'END { print NR }' file.txt

awk -F, '{ print $1, $3 }' data.csv
free -m | awk '/Mem:/ { print "Used:", $3 "MB" }'

awk 'BEGIN { FS=":"; OFS="\t" }
     { print $1, $7 }
     END { print "done" }' /etc/passwd
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty `$1` / wrong columns | Separator | `-F','` or `-F':'`; watch quoted CSV |
| Off-by-one fields | Leading spaces / empty fields | `NF`; try `awk -F'[ ]+'` |
| Totals wrong | Forgot `END` | Accumulate in body, print in `END` |
| Locale weird numbers | Decimal comma | `LC_ALL=C awk …` |

## Real-World Applications
Pulling columns from `/etc/passwd`, summing access-log bytes, and quick `free`/`df` one-liners in incident shells.

## Pros/Cons or Trade-offs
- **Pro:** Fast streaming column tool; present everywhere.
- **Con:** Naive CSV/JSON handling; dialect differences (gawk vs mawk).
- **Trade-off:** Keep work *inside* awk vs shell loops calling awk per line.

## Comparison
vs [[grep]]: grep finds lines; awk reshapes fields. vs [[jq]]: jq for JSON. vs Python: use Python for quoted CSV and complex state.

## Mistakes to Avoid
- Parsing quoted CSV with `-F,`.
- Relying on gawk-only flags (`/regex/i`) in portable scripts.
- Wrapping awk in a shell loop over every line of a huge file.
