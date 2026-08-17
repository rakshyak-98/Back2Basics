[[Operating System]] [[MBR]] [[Boot/UEFI]] [[Persistent Block Storage]] [[logical partitions]] [[Boot/UEFI (2)]]

# MBR(Master Boot Record)

> Alias for the Master Boot Record — first-sector BIOS boot structure with partition table and 446-byte code field; canonical detail lives in [[MBR]].





## Interview Relevance
Same as [[MBR]]: know LBA 0 is not a file, signature `0xAA55`, and UEFI/GPT relationship — including protective/hybrid MBR when CSM is enabled.

## Sources
- [Wikipedia — Master boot record](https://en.wikipedia.org/wiki/Master_boot_record) — overview
- UEFI specification — legacy BIOS compatibility — overview

## Key Concepts
- **Not a file:** the MBR is LBA 0 on disk.
- **512-byte sector** ending in **0xAA55**.
- **Four primary partitions;** extended type for [[logical partitions]].
- **Tiny boot code:** only enough to jump to VBR or GRUB stage2.

## Technical Details
Corrupt partition entries or overwritten boot code produce “Operating system not found” on legacy firmware paths.

UEFI systems may still contain an MBR-style protective or hybrid layout on GPT disks when **CSM** is enabled ([[Boot/UEFI (2)]]).

Canonical layout and repair notes: [[MBR]].

## Real-World Applications
Imaging tools and `fdisk` still show “DOS/MBR” label style. Rescue media must distinguish boot-code damage from partition-table damage.

## Pros/Cons or Trade-offs
- **Pro:** Short alias note for the expanded name form.
- **Con:** Duplicate notes risk drift — prefer editing [[MBR]] first.

## Comparison
- Full treatment: [[MBR]].
- Modern firmware path: [[Boot/UEFI]].

## Mistakes to Avoid
- Editing only this alias and leaving [[MBR]] stale (or the reverse).
- Treating protective GPT MBR as a real four-partition DOS layout to rewrite casually.
