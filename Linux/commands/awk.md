```text
awk 'pattern { action }' file:
```

## How to print user and their belonging groups

```bash
getent passwd | awk -F: '{print $1}' | while read user; do
	echo -n "$user: "
	groups "$user" | cut -d: -f2
done
```

```bash
# Show only user and shell
awk -F: '{print $1 "\t→ " $7}' /etc/passwd

# Show memory usage in MB
free -m | awk '/Mem:/ {print "Used:", $3"MB"}'

# Extract IPs from logs
journalctl | awk '/Failed password/ {print $11}'

# Show biggest files in current directory
ls -l | awk 'NR>1 {print $5, $9}' | sort -nr | head

# Convert CSV to space-separated
awk -F, '{print $1, $3}' data.csv

# Running total
seq 10 | awk '{sum += $1; print $1, "→", sum}'

```

- if no pattern -> runs on every line
- if no action -> defaults to `{ print $0 }` (print whole line).
- input is automatically split into fields: `$1` `$2` `$3`

> print 2nd column of every line

```bash
awk '{ print $2 }' file.text
```

|Symbol|Meaning|Example|
|---|---|---|
|`$0`|whole line|`print $0`|
|`$1,$2..`|columns (space-separated by default)|`print $1,$3`|
|`NF`|number of fields in current line|`print $NF`|
|`NR`|current line number|`NR==10`|
|`FS`|input field separator|`-F:` or `FS=":"`|
|`OFS`|output field separator|`OFS=" → "`|
|`BEGIN`|run before any input|`BEGIN {print "Start"}`|
|`END`|run after all input|`END {print "Total:", sum}`|
|`/regex/`|pattern match|`/error/i` (case-insensitive)|

> [!NOTE]
> - by default `awk` split each line on white-space (space or tab).
> - Text processing tool for line by line parsing.
> - patterns scanning + processing (fields, columns, regex, etc.).
 
```sh
awk 'pattern { action }' file;
```

### Common built in variables
| Variable | Description                        |
| -------- | ---------------------------------- |
| `$0`     | Entire line                        |
| `$1,$2…` | Fields (by default split by space) |
| `NR`     | Line number                        |
| `NF`     | Number of fields in line           |
| `FS`     | Field separator                    |
| `OFS`    | Output field separator             |
```sh
awk -F, '{ print $1 }' file.csv; # change delimiter
```

```sh
awk 'BEGIN { init_code } 
     condition { action_code } 
     END { cleanup_code }'
```


### The 10 Commands You’ll Use 95% of the Time

Run these one by one in your terminal:

```bash
# 1. Print 2nd column
echo "apple 42 red" | awk '{print $2}'

# 2. Print multiple columns
echo "apple 42 red big" | awk '{print $1, $4}'

# 3. Print last column
awk '{print $NF}' /etc/passwd

# 4. Print second-to-last column
awk '{print $(NF-1)}' /etc/passwd

# 5. Only lines containing "bash"
awk '/bash/ {print $0}' /etc/passwd

# 6. Only lines where column 3 > 100
awk '$3 > 100 {print $0}' data.txt

# 7. Add all values in column 2
awk '{sum += $2} END {print "Total =", sum}' numbers.txt

# 8. Count lines (like wc -l)
awk 'END {print NR}'

# 9. Print line numbers
awk '{print NR, $0}' file.txt

# 10. Use custom field separator (e.g. colon in /etc/passwd)
awk -F: '{print $1, $7}' /etc/passwd
```

