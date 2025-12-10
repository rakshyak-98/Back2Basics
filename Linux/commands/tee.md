|What you want|Command|
|---|---|
|See output + save to file|`ls -la \| tee listing.txt`|
|Save and keep running the pipeline|`docker logs myapp \| tee docker.log \| grep ERROR`|
|Append instead of overwrite|`htop -n 5 \| tee -a monitor.log`|
|Save with sudo but run command as normal user|`cat /etc/shadow \| tee /tmp/shadow.txt` → fails `sudo cat /etc/shadow \| tee /tmp/shadow.txt` → works Better: `sudo cat /etc/shadow \| sudo tee /tmp/shadow.txt`|
|Write to multiple files at once|`echo "Hello" \| tee file1.txt file2.txt file3.txt`|
|Save root-owned file from non-root command|`echo "nameserver 8.8.8.8" \| sudo tee /etc/resolv.conf`|
|Live tail + save forever|`journalctl -f \| tee journal-backup.log`|
|Debug a long pipeline without breaking it|`curl -s https://api.example.com \| tee /dev/stderr \| jq .`|
|Suppress the screen output, only save to file|`command \| tee file.txt \| cat > /dev/null`|
|Colorized output in terminal AND in file (2025 trick)|`git log --oneline --graph --all \| tee git-history.txt` (colors are preserved!)|
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