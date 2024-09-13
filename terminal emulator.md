- terminal emulator use a communication mechanism called a [[TTY (teletypewriter)]] (psuedo-tty), which consists of two ends: the master (or primary) side, managed by the terminal emulator, and the slave (or secondary) side, where the shell or other command-line applications run. This step allows for bidirectional communication between the user interface and the shell.

### Input and Output handling
- when a user types a command, the terminal emulator captures this input and sends it to the shell via the PTY's standard input (STDIN). 
- Conversely when the shell produces output (such as command results), this data is sent back to the terminal emulator through the PTY's standard output (STDOUT) channel. The terminal emulator then formats and displays this output on the screen.