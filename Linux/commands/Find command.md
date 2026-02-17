## Only change permission of file in current directory

```bash
find . -type -f -exec chmod 644 {} +
```

|Part|Meaning|
|---|---|
|`{}`|Placeholder for each file/path that `find` discovers|
|`+`|“Append as many filenames as possible to this one command” (like xargs)|
|`\;`|Old way: “Run the command once per file” (slow — avoid it)|

```sh
find . -name "*.log" -delete;
```
- delete `.log` files, descending into subdirs first.
- removes subdirs before parent
- prevents modifying symlinks before their contents are processed.

```bash
## files 
find ./ -name '*.txt'
stat [filename]; # to see more info on the file.

# find modified within last 30 days in directory and subdirectory.
find /home -mtime -30; 
find [path] -type f -name [file name];

# find all empty directory.
find [directory] -type d -empty;

# find directory and subdirectory owned by root
find <directory> -user root;
find <path> -maxdepth 2 -mindepth 2 -type [d|f|l] -name <sourcename> -delete.
find /path -type f -empty;
find /path -mtime -7;
find /path -name "*.log" -delete;
find /path -name "*.log" -exec rm {} \;

```

```sh
find . -size +10M;
find . -empty; # find empty files and directory

find . -user john; # files owned by user 'john'
find . -perm 6444; # files with exact permission 644

```

```sh
find . -exec rm {} \; # Execute commands `rm` on found files
```
