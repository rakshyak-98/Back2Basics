- read from `stdin` 
- writes to both `stdout` and Files
- useful for logging output while still displaying it.
tee - command is used to redirect the output of a command to a file, while still displaying it on the terminal. It is named after the T-spliter used in plumbing, which splits water into two directions.

```sh
<command> | tee file.txt;
ls -l | tee files.txt; # save output file and see it live.
echo "log lie" | tee -a log.txt; # append instead of overwrite.
echo "config" | tee a.txt b.txt c.txt; # save output to multiple files.
```

```bash
```