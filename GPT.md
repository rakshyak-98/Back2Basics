- GUID Partition Table
- Globally Unique Identifiers, Each partition in a GPT scheme is assigned a unique identifier, which helps in managing and recognizing partitions across different systems and operating environments.
- partitioning scheme that addresses the limitations of the older Master Boot Record system.
- GPT is integral to the [[UEFI]] standard, replacing the traditional BIOS.
- GPT can handle drives larger than 2 terabytes supporting sizes up to 9.4 zettabytes due to its use of 64-bit logical block addressing.

> [!INFO] [[MBR]] is limited to a maximum of 2TB.

- GPT allows for a significantly higher number of partitions. While MBR limits users to four primary partitions (or up to 26 if using extended partitions).

> [!INFO] GPT support up to 128 partitions without the need for extended or [[logical partitions]].