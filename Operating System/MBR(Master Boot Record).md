[[Operating System]] [[MBR]] [[Boot/UEFI]] [[Persistent Block Storage]]

# MBR(Master Boot Record)

> This note aliases the Master Boot Record — the first-sector BIOS boot structure with partition table and 446-byte code field; see [[MBR]] for full detail.

The **Master Boot Record** is not a file — it is LBA 0 on a disk. Corrupt partition entries or overwritten boot code produce “Operating system not found” on legacy firmware paths.

Key facts:

- 512-byte sector, signature **0xAA55** at end.
- Four primary partitions; extended type for [[logical partitions]].
- Boot code too small for modern features — only enough to jump to volume boot record or GRUB stage2.

UEFI systems may still contain an MBR-style protective or hybrid layout on GPT disks when **CSM** is enabled ([[Boot/UEFI (2)]]).

Canonical detail: [[MBR]].

## Sources

- Wikipedia: [Master boot record](https://en.wikipedia.org/wiki/Master_boot_record)
- UEFI specification — legacy BIOS compatibility
