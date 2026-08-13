[[process]] [[Memory management]] [[commands/gdb]]

# hax dump

> A hex dump displays raw bytes of a file or memory region — essential for inspecting magic headers, corrupted records, and protocol payloads.

## Tools

```bash
# Classic
xxd file.bin | head
hexdump -C file.bin | head

# od
od -Ax -tx1z -N 256 file.bin

# strings for embedded text
strings -n 8 binary | head
```

## Partial read

```bash
dd if=file.bin bs=1 skip=512 count=64 2>/dev/null | xxd
```

## Compare binaries

```bash
cmp -l a.bin b.bin | head
diff <(xxd a.bin) <(xxd b.bin)
```

## Related

[[commands/diff]] · [[management/ELF (Editabl Linkable File)]] · [[commands/gdb]]

## Sources

- `man 1 xxd`, `man 1 hexdump`
