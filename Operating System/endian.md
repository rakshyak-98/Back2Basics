[[Operating System]] [[TCP]] [[ELF (Editabl Linkable File)]] [[SYSV (System V)]]

# endian

> Endianness is byte order in memory for multi-byte values — big puts the high byte first; little puts the low byte first.

---

## Mental model

**Say it in one breath:** The number `0x12345678` is four bytes; endianness decides whether memory reads `12 34 56 78` or `78 56 34 12`.

```txt
Address:  0    1    2    3
Big:     12   34   56   78     (MSB at lowest address)
Little:  78   56   34   12     (LSB at lowest address)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Big-endian** | MSB at lowest address | “Network byte order is big-endian.” |
| **Little-endian** | LSB at lowest address | “x86/x86-64 are little-endian.” |
| **Host order** | What this CPU uses | “Never write raw structs to the wire.” |
| **Network order** | Big-endian on the wire | “`htonl` / `ntohl` before send/after recv.” |
| **NUXI problem** | Same bytes, different ints | “Cross-endian dumps look like swapped halves.” |
| **BE/LE file formats** | On-disk convention | “PNG/JPEG mark order; ELF has EI_DATA.” |

### How the story goes (4 steps)

1. **Decide a protocol order** — almost always big-endian for classic IP protocols.
2. **Convert on the edge** — host → network on send; network → host on receive.
3. **Keep wire formats explicit** — fixed-width fields, documented endian.
4. **Test on both** — or fuzz with byte-swapped fixtures.

---

## Standard config / commands

```c
#include <arpa/inet.h>
uint32_t be = htonl(0x12345678);  // host → network (big)
uint32_t host = ntohl(be);        // network → host

// Fixed decode without assuming host
uint32_t rd_be(const uint8_t *p) {
  return ((uint32_t)p[0] << 24) | (p[1] << 16) | (p[2] << 8) | p[3];
}
```

```bash
# What is this machine?
lscpu | grep -i 'Byte Order'
python3 -c "import sys; print(sys.byteorder)"

# ELF endian marker
readelf -h ./binary | grep -i data
# ELFDATA2LSB / ELFDATA2MSB
```

| Knob | Why it matters |
|------|----------------|
| `htons/htonl` vs `htobe16` | Portability helpers — use them on every multi-byte field |
| Packed structs on the wire | Padding + endian bugs compound |
| Protobuf / JSON | Mostly hide endian — still care for custom binary |
| DMA / device registers | Hardware docs specify order; trust the datasheet |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Magic number looks swapped | Hex dump first bytes | Convert with correct endian reader |
| Works on x86, fails on BE CPU | Assumed host order | Use explicit BE/LE codecs |
| Checksums fail | Field order before hash | Match RFC byte order |
| “Random” IPv4 in logs | Forgot `ntohl` | Convert before printf |
| File won’t parse | Format endian vs host | Read spec; don’t `fread` into structs blindly |

---

## Gotchas

> [!WARNING]
> **Casting `uint8_t*` to `uint32_t*`** also risks alignment faults — decode byte-wise or `memcpy` into an aligned integer.

> [!WARNING]
> **Bitfields and endian** interact in compiler-specific ways — avoid bitfields in wire structs.

> [!WARNING]
> **Unicode / text** is not “endian” the same way — UTF-16/32 need BOM or a known order.

> [!WARNING]
> **Bi-endian CPUs** exist — don’t hardcode; detect or fix the protocol.

---

## When NOT to use

- **Text protocols (JSON, HTTP headers)** — byte order of integers is not your problem.
- **Same-process in-memory structs on one arch** — native order is fine until you serialize.
- **When a schema IDL already defines encoding** — don’t invent a second endian convention.

---

## Related

[[TCP]] [[SYSV (System V)]] [[ELF (Editabl Linkable File)]] [[assembly language]] [[How to manipulate memory directly]] [[hax dump]]
