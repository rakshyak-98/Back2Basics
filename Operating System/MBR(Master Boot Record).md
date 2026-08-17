[[Operating System]] [[MBR]] [[Boot/UEFI]] [[Persistent Block Storage]] [[logical partitions]] [[Boot/UEFI (2)]]

# MBR(Master Boot Record)

> Alias for the Master Boot Record — first-sector BIOS boot structure with partition table and 446-byte code field; canonical detail lives in [[MBR]].

```txt
        MBR(Master Boot Re ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Same as [[MBR]]: know LBA 0 is not a file, signature `0xAA55`, and UEFI/GPT r…

## Sources
- [Wikipedia — Master boot record](https://en.wikipedia.org/wiki/Master_boot_record) — overview
- UEFI specification — legacy BIOS compatibility — overview

## Key Concepts
- **Not a file:** the MBR is LBA 0 on disk.
- **512-byte sector:** ending in **0xAA55**.
- **Four primary partitions;:** extended type for [[logical partitions]].
- **Tiny boot code:** only enough to jump to VBR or GRUB stage2.

## Technical Details
- Corrupt partition entries or overwritten boot code produce “Operating system …

- UEFI systems may still contain an MBR-style protective or hybrid layout on GP…

- Canonical layout and repair notes: [[MBR]].

## Mistakes to Avoid
- **Mistake:** Editing only this alias and leaving [[MBR]] stale (or the revers…
- **Mistake:** Treating protective GPT MBR as a real four-partition DOS layout …

## Pros/Cons or Trade-offs
- **Pro:** Short alias note for the expanded name form.
- **Con:** Duplicate notes risk drift — prefer editing [[MBR]] first.

## Comparison
- Full treatment: [[MBR]].
- Modern firmware path: [[Boot/UEFI]].


### Use cases
- Imaging tools and `fdisk` still show “DOS/MBR” label style
