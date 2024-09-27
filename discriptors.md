### File descriptors
- Standard input (stdin): file descriptor 0
- Standard output (stdout): file descriptor 1
- Standard Error (stderr): file descriptor 2

- when a program prints output, it writes to stdout, which is linked to the terminal or console by default.
- the kernel manages these file descriptors and routes output accordingly.