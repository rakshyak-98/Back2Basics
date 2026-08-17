[[process]] [[Memory management]] [[commands/gdb]] [[commands/diff]] [[management/ELF (Editabl Linkable File)]]

# hax dump

> A hex dump shows raw bytes of a file or memory region — use it to inspect magic headers, corrupted records, and protocol payloads.





## Interview Relevance
Debugging literacy: prove you can read binary with `xxd`/`hexdump`, compare blobs, and recognize when “garbage text” is actually a structured header (ELF magic, PNG, etc.).

## Sources
- `man 1 xxd`, `man 1 hexdump` — deep-dive

## Core Definition
Hex dump tools print offsets, hexadecimal bytes, and often an ASCII sidebar. They are the first step before deeper tools (`readelf`, Wireshark, gdb) when you only have a blob.

## Key Concepts
- **Offset + hex + ASCII:** Standard three-column view (`hexdump -C`, `xxd`).
- **Partial windows:** `dd` + `xxd` to sample mid-file without loading everything.
- **Binary diff:** `cmp -l` or `diff` of two `xxd` streams.
- **strings:** Complementary — extract printable runs, not a full layout view.

## Technical Details
```bash
xxd file.bin | head
hexdump -C file.bin | head
od -Ax -tx1z -N 256 file.bin
strings -n 8 binary | head

dd if=file.bin bs=1 skip=512 count=64 2>/dev/null | xxd

cmp -l a.bin b.bin | head
diff <(xxd a.bin) <(xxd b.bin)
```

## Real-World Applications
A “corrupt” upload starts with unexpected bytes — `xxd` shows `7f 45 4c 46` (ELF) instead of JSON, revealing a binary was saved as the artifact.

## Pros/Cons or Trade-offs
- **Pro:** Universal, works on any file, no schema required.
- **Con:** Slow and noisy on huge files; structured parsers (`readelf`, `pcap`) beat eyeballing once you know the format.

## Comparison
vs `strings`: strings finds text; hex dump shows layout and non-printables. vs gdb/`x` command: gdb dumps process memory live; hex dump tools target files (or core snapshots). vs [[management/ELF (Editabl Linkable File)]]: ELF notes interpret headers; hex dump is the raw view underneath.

## Mistakes to Avoid
- Dumping multi-gigabyte files to the terminal without `head`/`-N`.
- Assuming ASCII sidebar “words” are trustworthy without checking surrounding bytes.
- Using hex dump alone for ELF/DWARF when `readelf`/`llvm-readobj` exist.
