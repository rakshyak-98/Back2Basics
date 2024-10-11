In Linux and Unix-like systems, exit codes (also known as exit statuses or return codes) are numeric values returned by a command or a program to indicate the outcome of its execution. A value of 0 typically indicates success, while non-zero values indicate various types of errors or abnormal conditions.

Here are some common exit codes along with their meanings:

- **0**: Success
- **1**: General error
- **2**: Misuse of shell builtins
- **126**: Command invoked cannot execute (permission issue or not an executable)
- **127**: Command not found
- **128**: Invalid argument to exit
- **128 + N**: Fatal error signal "N" (e.g., 128 + 9 = 137 indicates a SIGKILL)
- **130**: Script terminated by Control-C
- **137**: Process terminated by Control-C (128 + 9)
- **139**: Segmentation fault (invalid memory reference)
- **143**: Process terminated by Control-C (128 + 15)
- **255**: Exit status out of range or undefined