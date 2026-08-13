[[Operating System]] [[TCP]] [[Linux/management/ELF (Editabl Linkable File)]] [[SYSV (System V)]]

# Endian

> Endianness defines which byte of a multi-byte integer sits at the lowest memory address — mismatches between CPU, wire protocol, and file format cause silent corruption unless converted.

**Little-endian:** least significant byte first (x86, x86-64, most ARM in practice). **Big-endian:** most significant byte first (many network protocols, some legacy CPUs).

## Where it appears

| Context | Convention |
|---------|------------|
| [[TCP]] / IP headers | Big-endian on the wire |
| [[ELF (Editabl Linkable File)]] | Header declares `EI_DATA` |
| User structs on disk | Must specify layout; `#pragma pack` pitfalls |

```c
uint32_t x = 0x01020304;
/* little-endian RAM: 04 03 02 01 */
```

Conversion: `htons`, `htonl`, `le32toh` / `be32toh` (BSD/glibc).

## Debugging

Hex dumps compared to protocol docs, wrong magic in binaries, checksum failures on network payloads — all classic endian bugs.

## Sources

- Stevens, *UNIX Network Programming* — byte ordering
- Wikipedia: [Endianness](https://en.wikipedia.org/wiki/Endianness)
- ELF specification — data encoding
