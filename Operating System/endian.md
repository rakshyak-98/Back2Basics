[[Operating System]] [[TCP]] [[Linux/management/ELF (Editabl Linkable File)]] [[SYSV (System V)]]

# Endian

> Endianness defines which byte of a multi-byte integer sits at the lowest address — CPU, wire, and file formats must agree or you get silent corruption.

## Interview Relevance

Network and binary formats: network byte order is big-endian; x86 is little-endian; show `htons`/`ntohl` fluency.

## Sources

- Stevens, *UNIX Network Programming* — byte ordering — deep-dive
- [Wikipedia — Endianness](https://en.wikipedia.org/wiki/Endianness) — overview
- ELF specification — data encoding — deep-dive

## Key Concepts

- **Little-endian:** LSB first (x86, typical ARM).
- **Big-endian:** MSB first (many wire protocols).
- **Network order:** [[TCP]]/IP headers are big-endian on the wire.
- **Declared layouts:** ELF `EI_DATA`; on-disk structs must specify endianness.

## Technical Details

| Context | Convention |
|---------|------------|
| [[TCP]] / IP headers | Big-endian on the wire |
| [[Linux/management/ELF (Editabl Linkable File)]] | Header declares `EI_DATA` |
| User structs on disk | Must specify layout; packing pitfalls |

```c
uint32_t x = 0x01020304;
/* little-endian RAM: 04 03 02 01 */
```

Conversion: `htons`, `htonl`, `le32toh` / `be32toh`.

## Real-World Applications

Socket code, custom binary protocols, firmware image parsers, and cross-compiling ELF for different `EI_DATA`.

## Pros/Cons or Trade-offs

- **Native endian:** fast loads/stores on that CPU.
- **Fixed wire endian:** portable protocols; conversion cost on LE hosts.
- **Trade-off:** convert at edges vs store everything in network order.

## Comparison

- vs alignment/packing: related binary-layout bugs, different root cause.
- vs text protocols: JSON/UTF-8 avoid integer endian issues.

## Mistakes to Avoid

- Casting wire buffers to host structs without conversion.
- Checking magic numbers without considering byte order.
- Mixing LE file formats with BE CPUs (or vice versa) without tests.
