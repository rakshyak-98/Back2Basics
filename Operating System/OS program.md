[[Operating System]] [[linker]] [[interpreter]] [[system call]] [[Runtime Environment]] [[process]]

# OS program

> An OS program is an executable image the kernel loads into a [[process]] — ELF binary, script with shebang, or dynamic shared object run by the loader.

Lifecycle:

```txt
User invokes path → execve() → kernel reads ELF headers
→ maps segments → sets up stack/heap → start (e.g. _start → main)
→ program runs via [[system call]] until exit
```

Formats: ELF on Linux ([[Linux/management/ELF (Editabl Linkable File)]]), PE on Windows. Scripts delegate to [[interpreter]] binaries.

The **runtime** ([[runtime]], [[Runtime Environment]]) supplies libc, thread startup, and dynamic linking after the kernel hands off control.

## Sources

- Bryant & O’Hallaron, *Computer Systems*
- Linux `execve(2)`, ELF specification
- Wikipedia: [Executable](https://en.wikipedia.org/wiki/Executable)
