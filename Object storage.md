[[AWS S3]]

Object storage is inexpensive compared to other cloud storage options. This allows cloud databases to store data that's queried less often on cheaper, higher-latency storage while serving while serving the working set from memory, SSDs, and NVMe.

Object storage provides multi-zone, dual-region, or multi-region replication with very high durability guarantees. This also allow databases to bypass inter-zone network fees.
Storing data from multiple database in the same object store can simplify data integration, particularly when open formats such as Parquet and Iceberg are used.

> Shifting the responsibility of transactions, leadership election, and replication to object storage. Systems that adpot object storage for replication must grapple with trade-offs, through. Notably, object stores have uch higher read and write latencies than local disks or virtual block devices such as Amazon EBS.