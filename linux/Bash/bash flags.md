|Flag|Description|
|---|---|
|`-a`|Automatically export all variables and functions that are modified or created.|
|`-b`|Notify when background jobs finish (print job status immediately).|
|`-c`|Read and execute commands from the following string (e.g., `bash -c "echo hello"`). Remaining arguments are assigned to positional parameters.|
|`-e`|Exit immediately if a command exits with non-zero status (errexit).|
|`-f`|Disable filename expansion (globbing).|
|`-h`|Remember locations of commands as they are looked up (hash functions before use).|
|`-i`|Force interactive shell (even if not attached to terminal).|
|`-k`|Place all keyword arguments in environment for commands (not just those before command name).|
|`-l`|Act as if invoked as a login shell (read `/etc/profile` and `~/.bash_profile`).|
|`-m`|Enable job control.|
|`-n`|Read commands but do not execute them (noexec; useful for syntax checking).|
|`-o option`|Enable the specified shell option (e.g., `-o vi` for vi mode; see full list below).|
|`-p`|Privileged mode (do not read profile files if effective UID ≠ real UID).|
|`-r`|Restricted shell (restricted mode; limits features).|
|`-t`|Exit after reading and executing one command.|
|`-u`|Treat unset variables as errors when substituting (nounset).|
|`-v`|Print shell input lines as they are read (verbose).|
|`-x`|Print commands and their arguments as they are executed (xtrace; great for debugging).|
|`-B`|Enable brace expansion.|
|`-C`|Prevent output redirection from overwriting existing files (noclobber).|
|`-E`|If set, ERR trap is inherited by shell functions.|
|`-H`|Enable `!` style history substitution.|
|`-P`|Use physical directory structure for `cd` (do not follow symlinks).|
|`-T`|If set, DEBUG and RETURN traps are inherited by shell functions.|
|`--`|Signal end of options; treat remaining arguments as filenames/positional parameters.|