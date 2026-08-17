[[process]] [[Memory management]] [[commands/gdb]] [[commands/diff]] [[management/ELF (Editabl Linkable File)]]

# hax dump

> A hex dump shows raw bytes of a file or memory region — use it to inspect magic headers, corrupted records, and protocol payloads.

```txt
        hax dump ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Debugging literacy: prove you can read binary with `xxd`/`hexdump`, compare b…

## Sources
- `man 1 xxd`, `man 1 hexdump` — deep-dive

## Key Concepts
- **Offset + hex + ASCII:** Standard three-column view (`hexdump -C`, `xxd`).
- **Partial windows:** `dd` + `xxd` to sample mid-file without loading everything.
- **Binary diff:** `cmp -l` or `diff` of two `xxd` streams.
- **strings:** Complementary — extract printable runs, not a full layout view.


- **Core:** Hex dump tools print offsets, hexadecimal bytes, and often an ASCII sidebar

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

## Mistakes to Avoid
- **Mistake:** Dumping multi-gigabyte files to the terminal without `head`/`-N`
- **Mistake:** Assuming ASCII sidebar “words” are trustworthy without checking …
- **Mistake:** Using hex dump alone for ELF/DWARF when `readelf`/`llvm-readobj`…

## Pros/Cons or Trade-offs
- **Pro:** Universal, works on any file, no schema required.
- **Con:** Slow and noisy on huge files; structured parsers (`readelf`, `pcap`) beat eyeballing once you know the format.

## Comparison
- vs `strings`: strings finds text


### Use cases
- A “corrupt” upload starts with unexpected bytes
