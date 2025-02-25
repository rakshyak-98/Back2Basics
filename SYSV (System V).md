Unix System V is one of the first commercial versions of the Unix operating system.

SYSV (System V) refers to System V ABI, which is a standard for UNIX-like operating systems.
ABI (Application Binary Interface)

The System V ABI defines conventions for binary compatibility, including:
- Function calling conventions
- Register usage
- Stack layout
- Dynamic linking conventions

#### Why is this important?
- Ensures binary compatibility across different Linux distributions.
- Helps the dynamic linker `ld.so` load and run the binary correctly.
- If a binary was compiler using a non-standard ABI (e.g., `GNU` extensions), it might be incompatible with certain systems.

> [!INFO] Some binary may use different ABI (e.g., `GNU` `MIPS` `ARM`), but those are architecture-dependent.

```shell
readelf -h gopls; # check the ABI of an ELF binary in detail
```
- Look for
```txt
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
```

```shell
objdump -f gopls; # this will confirm that the binary is following System V ABI.
```
