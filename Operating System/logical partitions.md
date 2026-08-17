[[Operating System]] [[MBR]] [[Persistent Block Storage]] [[cgroup (Control Group)]] [[Boot/UEFI]]

# Logical partitions

> Logical partitions extend MBR’s four primary slot limit by nesting partitions inside an extended container — legacy layout largely replaced by GPT on UEFI systems.





## Interview Relevance
Disk layout history: primary vs extended vs logical, MBR 2 TiB limit, and why GPT removed the need.

## Sources
- [Wikipedia — Extended boot record](https://en.wikipedia.org/wiki/Extended_boot_record) — overview
- [Wikipedia — GUID Partition Table](https://en.wikipedia.org/wiki/GUID_Partition_Table) — overview
- Microsoft documentation — disk partitioning — overview

## Key Concepts
- **Four primary slots** on [[MBR]].
- **Extended container** holds chained logical partitions (EBRs).
- **Device names:** often `/dev/sda5+` for logicals.
- **Modern path:** GPT on [[Boot/UEFI]] — many primaries, no extended gymnastics.

## Technical Details
Tools (`fdisk`, `parted`) expose logicals as higher minor numbers. Fragility of EBR chains and the ~2 TiB MBR cap pushed GPT adoption on [[Persistent Block Storage]].

Conceptual analogy only: dividing machine resources with [[cgroup (Control Group)]] — different domain, similar “partition the namespace” idea.

## Real-World Applications
Old BIOS disks, rescue of legacy dual-boot layouts, and imaging tools that still emit MBR+logical schemes.

## Pros/Cons or Trade-offs
- **Pro:** More than four partitions on classic MBR.
- **Con:** Fragile EBR chains; size limits; confusing numbering.
- **Trade-off:** keep MBR for old firmware vs migrate to GPT.

## Comparison
- vs GPT partitions: flat table vs extended/logical nesting.
- vs [[MBR]] primary-only: logicals are the overflow mechanism.

## Mistakes to Avoid
- Deleting an extended partition and wiping all logicals inside.
- Assuming `/dev/sda5` is “fifth primary.”
- Using logical-partition schemes on new UEFI-only GPT systems.
