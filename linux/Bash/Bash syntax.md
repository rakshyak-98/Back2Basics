### Command manipulation
```shell
echo "Today is ${date}"
mkdir new_dir && cd new_dir # conditional execution
diff <(ls dir1) <(ls dir2);
```

```
(cd /tmp && ls); # Executes commands in a separate subshell
```
- This runs the `cd` and `ls` commands in a sub-shell, so the working directory in the current shell remains unchanged.


## Command history expansion
```shell
!!; # Repeats the last executed command;
!-2 # Executes the second-to-last command in history;
```

```shell
echo ${my_var:-"default value"}  # Prints "default value" if my_var is unset.
echo ${my_var:0:3}  # Extracts the first 3 characters from my_var.
```

In Bash, **set flags** (or options) allow you to change the behavior of the shell. You can enable or disable these flags using the `set` command. Here’s a list of some commonly used set flags in Bash:

### Common Bash Set Flags

1. **`-e`**: Exit immediately if a command exits with a non-zero status. This is useful for error handling in scripts.

2. **`-u`**: Treat unset variables as an error when substituting. This helps catch mistakes where a variable might not be initialized.

3. **`-o pipefail`**: This causes a pipeline to return the exit status of the last command that returned a non-zero status, or zero if no command fails. This helps in error detection in pipelines.

4. **`-x`**: Print each command before executing it. This is useful for debugging.

5. **`-n`**: Read commands but do not execute them. This is a way to check for syntax errors in scripts.

6. **`-v`**: Print shell input lines as they are read. This is another debugging tool.

7. **`-f`**: Disable file name generation (globbing). This prevents wildcard expansion.

8. **`-h`**: Remember and perform hash lookup on commands. This speeds up the execution of commands by avoiding repeated searches in the path.

9. **`-p`**: Use the `privileged` mode, which is often used in setuid scripts to execute with the privileges of the script's owner.

10. **`-a`**: Mark variables and functions to be exported automatically to the environment of subsequently executed commands.

### How to Use Set Flags
You can enable or disable these flags using the `set` command as follows:
```bash
set -e      # Enable exit on error
set +e      # Disable exit on error
set -u      # Enable error on unset variables
set +u      # Disable error on unset variables
```

### Example
Here’s a simple example of using flags in a script:
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, unset vars error, and fail on pipe errors

# Example commands
echo "This script will exit on error."
ls non_existent_file  # This will cause the script to exit
```

## Configuration setup
[[Kafka configuration]]
```shell
if [[ "$*" = *"/opt/bitnami/scripts/kafka/run.sh"* || "$*" = *"/run.sh"* ]]; then
    info "** Starting Kafka setup **"
    /opt/bitnami/scripts/kafka/setup.sh
    info "** Kafka setup finished! **"
fi
```
- this script checks if a specific script (`run.sh`) is part of the command line arguments, and if so, it runs a kafka setup script.

```shell
if [[ "$*" = *"/opt/bitnami/scripts/kafka/run.sh"* || "$*" = *"/run.sh"* ]]; then
```
- `$*` -> represents all command-line arguments passed to the script.
- `[[ "$*" = *"/opt/bitnami/scripts/kafka/run.sh"* || "$*" = *"/run.sh"* ]]` checks if any argument contains `/opt/bitnami/scripts/kafka/run.sh` or `run.sh`
- the `*` wildcard makes it a sub-string match.
