### **Ignoring Commands in History**
- **`HISTIGNORE`**: Excludes certain commands from being saved in history.
```shell
export HISTIGNORE="ls:cd:pwd"; # prevent from being saved to history.
export HISTCONTROL=ignoreboth;
```

- `HISTORYCONTROL` Controls what gets saved to history 
 `ignorespace`, `ignoredups`, `ignoreboth` 

```shell
history -a; # Appends the history of the current session to the history file
```

## Command history expansion
```shell
!!; # Repeats the last executed command;
!-2 # Executes the second-to-last command in history;
```

```shell
echo ${my_var:-"default value"}  # Prints "default value" if my_var is unset.
echo ${my_var:0:3}  # Extracts the first 3 characters from my_var.
```

## History manipulation
```shell
HISTORYCONTROL=ignoredups:erasedups; # Avoid duplicate history entries.
```

```shell
!?install; # executes the last command that contains the word "install"
^git^git-lfs; # Replaces the first occurrence of git with git-lfs in the last executed command
```

```shell
!!:s/old/new/ # replace old with new in the last command.
^old^new^ # quick replace old with new in the last command.
```
#### Previous command arguments
```shell
!$; # last argument of the previous command.
!^ # first argument of the previous comamnd.
```

```shell
fc -l; # list history commands
fc -e nano n # edit history entry n in nano.
```