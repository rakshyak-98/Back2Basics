## Node REPL debugger operation


| Command                | Shortcut   | What it does                                        | Example use case                            |
| ---------------------- | ---------- | --------------------------------------------------- | ------------------------------------------- |
| `continue`             | `c`        | Continue running until next `debugger;` or end      | Skip to the next breakpoint                 |
| `next`                 | `n`        | Step over (next line, don't enter functions)        | Move line-by-line without diving into calls |
| `step`                 | `s`        | Step into (enter function calls)                    | Debug inside a function                     |
| `out`                  | `o`        | Step out (finish current function and return)       | Get out of a deep call stack                |
| `pause`                |            | Pause execution right now (like Ctrl+C but cleaner) | Force a break when running                  |
| `backtrace`            | `bt`       | Show call stack (where you are)                     | Understand how you got here                 |
| `list`                 | `l`        | Show surrounding source code (default 5 lines)      | `l 10` → show around line 10                |
| `list(10)`             |            | Show more context (e.g. 10 lines before/after)      | See bigger chunk of code                    |
| `repl`                 |            | Enter REPL mode (inspect & run JS expressions)      | Check variable values (see below)           |
| `watch('x')`           |            | Auto-print value of expression on every stop        | `watch('sum')` to monitor a variable        |
| `unwatch('x')`         |            | Stop watching an expression                         | Clean up watchers                           |
| `break <line>`         | `b <line>` | Set breakpoint at line number                       | `b 12` → break at line 12                   |
| `break fnName`         |            | Set breakpoint at function start                    | `break calculate`                           |
| `clearBreak <num>`     |            | Remove breakpoint (see list with `breakpoints`)     |                                             |
| `breakpoints`          |            | List all active breakpoints                         |                                             |
| `exec <code>`          |            | Run JS code in current context (rarely needed)      |                                             |
| `help`                 | `h`        | Show all available commands                         | Quick reference                             |
| `.exit` / `quit` / `q` |            | Exit the debugger                                   | Finish session                              |