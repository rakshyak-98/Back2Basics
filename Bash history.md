### **Ignoring Commands in History**
- **`HISTIGNORE`**: Excludes certain commands from being saved in history.
```shell
export HISTIGNORE="ls:cd:pwd"; # prevent from being saved to history.
export HISTICONTROL=ignoreboth;
```

- `HISTORYCONTROL` Controls what gets saved to history 
 `ignorespace`, `ignoredups`, `ignoreboth` 

```shell
history -a; # Appends the history of the current session to the history file
```