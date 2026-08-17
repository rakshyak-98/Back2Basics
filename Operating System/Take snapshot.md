[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[fsync]] [[RAM and Swap memory]]

# Take snapshot

> A storage snapshot is a point-in-time view of a volume — copy-on-write or redirect-on-write — so you can roll back or clone without copying every block up front.

```txt
        Take snapshot ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Backup/DR reviews: crash-consistent vs application-consistent snapshots, a…

## Sources
- [Wikipedia — Snapshot (computer storage)](https://en.wikipedia.org/wiki/Snapshot_(computer_storage)) — overview
- LVM2 documentation — snapshots — deep-dive
- AWS EBS snapshot documentation — overview

## Key Concepts
- **Point-in-time view:** COW / ROW deferred copy of changed blocks.
- **Providers:** Btrfs, ZFS, LVM, cloud volume APIs, hypervisors.
- **Consistency:** quiesce + [[fsync]] for application-consistent
- **Not a backup:** still on the same failure domain until replicated off-box.

## Technical Details
```txt
Live volume → snapshot COW → mount clone for backup/forensics
```

- File systems and volume managers expose snapshot ops distinct from normal fil…
- VM “memory snapshots” (pause + RAM image) are a different mechanism related t…

- Related durable media: [[Persistent Block Storage]].

## Mistakes to Avoid
- **Mistake:** Calling local-only snapshots a disaster-recovery strategy
- **Mistake:** Snapshotting a busy database without flush/quiesce and expecting…
- **Mistake:** Letting snapshot chains grow unbounded until the pool fills

## Pros/Cons or Trade-offs
- **Pro:** Fast, space-efficient point-in-time copies.
- **Con:** Performance tax while COW is active; pool failure loses source + snaps.
- **Trade-off:** frequent snaps vs storage growth from changed blocks.

## Comparison
- vs full backup copy: backup usually leaves the box; snapshot may not.
- vs [[fsync]]: fsync makes one write durable; snapshot freezes a volume view.


### Use cases
- EBS snapshots before risky migrations, ZFS send/receive pipelines, and VM gol…
