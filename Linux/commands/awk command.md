- by default `awk` split each line on white-space (space or tab).
- Text processing tool for line by line parsing.
- patterns scanning + processing (fields, columns, regex, etc.).
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