[[commands]] [[grep]] [[jq]]

# awk

> awk walks a file line by line — match a pattern, run an action on fields.

---

## How it works

```txt
input lines ──► split on FS ──► match pattern? ──► run action ──► next line
                     BEGIN runs once first; END runs once last
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`$0` / `$1`…** | Whole line / fields | “`$3` is the third column after split.” |
| **`NF` / `NR`** | Field count / line number | “`NR` is the record number; `$NF` is the last field.” |
| **`-F` / `FS`** | Input separator | “`-F:` for `/etc/passwd`.” |
| **`BEGIN` / `END`** | Setup / teardown | “Sum in the body, print total in `END`.” |
| **No pattern** | Every line | “Defaults to run on all records.” |
| **No action** | Print match | “Pattern alone prints the line.” |

---


## Configuration and commands

```bash
# Columns
awk '{ print $2 }' file.txt
awk '{ print $1, $NF }' file.txt
awk -F: '{ print $1, $7 }' /etc/passwd

# Filter
awk '/error/ { print }' app.log
awk '$3 > 100 { print $0 }' data.txt

# Aggregate
awk '{ sum += $2 } END { print "Total =", sum }' numbers.txt
awk 'END { print NR }' file.txt          # line count
seq 10 | awk '{ sum += $1; print $1, "→", sum }'

# CSV / memory one-liners
awk -F, '{ print $1, $3 }' data.csv
free -m | awk '/Mem:/ { print "Used:", $3 "MB" }'

# Users → groups (primary + supplementary listing via groups)
getent passwd | awk -F: '{ print $1 }' | while read -r user; do
  echo -n "$user: "
  groups "$user" | cut -d: -f2
done
```

| Symbol | Meaning |
|--------|---------|
| `$0` | Whole line |
| `$1,$2…` | Fields (whitespace by default) |
| `NF` / `NR` | Fields this line / line number |
| `FS` / `OFS` | Input / output field separator |
| `/regex/` | Pattern match |

```bash
awk 'BEGIN { FS=":"; OFS="\t" }
     { print $1, $7 }
     END { print "done" }' /etc/passwd
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty `$1` / wrong columns | Separator | `-F','` or `-F':'`; watch quoted CSV |
| Off-by-one fields | Leading spaces / empty fields | `NF`; try `awk -F'[ ]+'` |
| Script “does nothing” | Pattern never matches | Drop pattern; print `$0` to verify |
| Totals wrong | Forgot `END` | Accumulate in body, print in `END` |
| Broken on large files | Shell loops around awk | Keep work *inside* awk |
| Locale weird numbers | Decimal comma | `LC_ALL=C awk …` |

---


## Gotchas

> [!WARNING]
> **Whitespace split collapses runs** — multiple spaces still make one split; empty columns disappear unless you set `FS` carefully.

> [!WARNING]
> **CSV with quotes is not a job for naive `-F,`** — use a real CSV tool or Python when fields contain commas.

> [!WARNING]
> **`/regex/i` is gawk** — portable awk may lack ignore-case flags; use `tolower($0) ~ /error/`.

---


## When not to use

- **Structured JSON** — [[jq]].
- **Multi-line records / complex state machines** — Python/Perl.
- **In-place edit of huge trees** — [[Find command]] + targeted editors.

---


## Related

[[grep]] [[jq]] [[sed]] [[commands]]

## Sources

- [Wikipedia — awk](https://en.wikipedia.org/wiki/awk)
