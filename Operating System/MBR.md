[[Operating System]] [[MBR]] [[Boot/UEFI]] [[logical partitions]] [[Persistent Block Storage]]

# MBR

> The Master Boot Record is the first 512-byte sector of a legacy BIOS-boot disk — partition table plus a tiny boot stub that chain-loads the real bootloader.

```txt
        MBR ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Storage/boot questions: MBR layout, four primary partitions, 2 TiB limit moti…

## Sources
- [Wikipedia — Master boot record](https://en.wikipedia.org/wiki/Master_boot_record) — overview
- GRUB documentation — BIOS boot installation — deep-dive

## Key Concepts
- **LBA 0 structure:** boot code + four partition entries + `0xAA55` signature.
- **Active partition:** BIOS hands off to the marked volume boot record.
- **Extended partitions:** enable [[logical partitions]] beyond four slots.
- **Legacy path:** [[Boot/UEFI]] + GPT superseded MBR for new large disks.

## Technical Details
```txt
Byte 0–445:   boot code (446 bytes max)
Byte 446–510: 4 × 16-byte partition entries
Byte 510–511: 0xAA55 signature
```

- Boot repair on MBR disks: reinstall stage1/stage2 to the boot sector or embed…
- CSM legacy mode and old images still use MBR.

## Mistakes to Avoid
- **Mistake:** Overwriting the MBR when you meant to rewrite only GRUB’s embedd…
- **Mistake:** Assuming MBR is required on modern UEFI-only systems
- **Mistake:** Ignoring protective MBR on GPT disks (first sector still looks “…

## Pros/Cons or Trade-offs
- **Pro:** Universal on old BIOS firmware; simple layout.
- **Con:** Four primary slots; ~2 TiB addressing limits; tiny boot code field.
- **Trade-off:** hybrid MBR on GPT for mixed BIOS/UEFI — complexity and footguns.

## Comparison
- Alias note: [[MBR]].
- vs [[Boot/UEFI]]: UEFI uses ESP + GPT; MBR is the BIOS-era first sector.


### Use cases
- Cloud images and VMs may still ship MBR for BIOS compatibility
