[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[fsync]]

# Take snapshot

> A storage snapshot is a point-in-time view of a volume — copy-on-write or redirect-on-write — letting you roll back or clone without copying every block upfront.

File systems (Btrfs, ZFS), LVM, cloud volume APIs, and VM hypervisors expose **snapshot** operations distinct from normal file copy.

## Consistency

Application-consistent snapshots quiesce writers or flush journals ([[fsync]]). Crash-consistent snapshots capture disk mid-write — databases may need recovery.

```txt
Live volume → snapshot COW → mount clone for backup/forensics
```

Snapshots are not backups until replicated off-box; they share pool with source on failure.

Related: [[Persistent Block Storage]], [[RAM and Swap memory]] (memory snapshots in VMs — different mechanism).

## Sources

- Wikipedia: [Snapshot (computer storage)](https://en.wikipedia.org/wiki/Snapshot_(computer_storage))
- LVM2 documentation — snap shots
- AWS EBS snapshot documentation
