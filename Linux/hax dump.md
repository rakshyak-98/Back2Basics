[[gdb]] [[webSocket]] [[Networking]]

# hax dump *(filename typo — see hexdump / xxd below)*

> One-line: **Hex dumps for binary inspection** — read wire formats, corrupt files, and WebSocket frames byte-by-byte. File is named `hax dump.md`; tools are **`hexdump`** and **`xxd`**.

## Mental model

A **hex dump** shows offset, hex bytes, and often ASCII sidebar. Every protocol debug eventually reduces to "what bytes actually crossed the wire?" — TLS hides payload, but framing errors, wrong endianness, and truncated reads show up in dumps first.

```
Offset   Hex bytes                    ASCII
0000000  48 65 6c 6c 6f              Hello
```

| Tool | Style | Best for |
|------|-------|----------|
| `hexdump -C` | Canonical (offset, hex, ASCII) | Default debug; compares to docs |
| `xxd` | Same family; `xxd -r` reverse | Make binary from hex edit |
| `od -Ax -tx1z` | POSIX | Minimal systems without hexdump |
| Wireshark | Packet hex pane | Full capture + decode |

## Standard config / commands

```bash
# Canonical dump — industry default
hexdump -C file.bin | head
hexdump -C file.bin | less

# First N bytes only
hexdump -C -n 256 file.bin

# Skip offset (inspect header vs body)
hexdump -C -s 0x10 -n 64 file.bin

# xxd (vim-friendly)
xxd file.bin | head
xxd -l 256 file.bin              # length limit
xxd -s 0x100 -l 64 file.bin      # skip + length

# Reverse: hex → binary (patch firmware/blob)
xxd -r patched.hex > patched.bin

# Compare two binaries quickly
hexdump -C a.bin > /tmp/a
hexdump -C b.bin > /tmp/b
diff -u /tmp/a /tmp/b

# Live stream (careful on pipes)
xxd /dev/urandom | head
```

**WebSocket / network context:** browser devtools and proxies show **frame payload** as hex when UTF-8 decode fails — binary opcodes, protobuf, or partial frames. Correlate with capture tools; don't guess protocol from hex alone.

**Strings first (when text embedded):**

```bash
strings file.bin | head
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbage ASCII column | Binary/compressed data | Expected; look for magic bytes at offset 0 |
| Wrong magic (`7f454c46` = ELF) | `hexdump -C -n 4` | Wrong file; truncation; swap endian |
| Dump all zeros | Sparse hole or real empty | `ls -l`; `stat`; check if preallocated |
| xxd -r corrupt output | Missing hex format | Input must be xxd/hexdump format |
| TLS traffic "hex" unreadable | Encrypted | Decrypt in Wireshark with keys; hexdump ciphertext low value |

**Common magic bytes:**

| Hex start | Type |
|-----------|------|
| `89 50 4E 47` | PNG |
| `FF D8 FF` | JPEG |
| `50 4B 03 04` | ZIP |
| `7F 45 4C 46` | ELF |
| `CA FE BA BE` | Java class / Mach-O fat |

## Gotchas

> [!WARNING]
> **`hexdump` huge files to terminal** — use `| less` or `-n`; dumping GB logs freezes SSH.

> [!WARNING]
> **PII/secrets in dumps** — tokens and keys appear in cleartext captures. Redact before tickets.

- **`hexdump` vs `od` flags differ** — scripts: prefer `hexdump -C` on GNU, test on target OS.
- **Line wrapping** — copy-paste hex for `xxd -r` must preserve column format.

## When NOT to use

- **Structured protocol decode** — use Wireshark dissectors, `protoc --decode`, language parsers.
- **Text config diff** — use [[diff]] on decoded UTF-8, not hex (unless encoding hunt).

## Related

[[gdb]] [[webSocket]] [[Networking]] [[diff]]
