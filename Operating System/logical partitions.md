[[Operating System]] [[MBR]] [[Persistent Block Storage]] [[cgroup (Control Group)]]

# Logical partitions

> Logical partitions extend MBR’s four primary slot limit by nesting partitions inside an extended container — a legacy layout largely replaced by GPT on UEFI systems.

**MBR** allows four **primary** partition entries. One can be an **extended** partition holding many **logical** partitions chained in linked EBRs. Tools (`fdisk`, `parted`) expose them as `/dev/sda5`, `/dev/sda6`, …

## Limits and modern alternative

- Complexity and fragility of EBR chains.
- 2 TiB disk size cap on MBR layout.
- **GPT** on [[Boot/UEFI]] machines supports dozens of primary partitions without extended/logical gymnastics.

Conceptually similar to dividing a machine into resource slices ([[cgroup (Control Group)]]) — different problem domain, same “partition the namespace” idea.

## Sources

- Wikipedia: [Extended boot record](https://en.wikipedia.org/wiki/Extended_boot_record), [GUID Partition Table](https://en.wikipedia.org/wiki/GUID_Partition_Table)
- Microsoft documentation — disk partitioning
