## Problem with Replication Lag

Leader replication: it requires all the writes to go through a single node, but read-only queries can go to any replica.

[[read-scaling Architecture]] increase the capacity for serving read-only requests simply by adding more followers.

Reasons why you might want to replication data:
- To scale out the number of machines that can sere read queries (and thus increase read throughput)

> If the data that you're replication does not change over time, then replication is easy: you just need to copy the data to every node once. All the difficulty in replication lies in handling changes to replicated data.

**All the difficulty in replication lies in handling changes to replication data.**

## Algorithms for replicating changes between nodes

[[Single-leader]]
[[Multi-leader]]
[[leaderless]]

**Synchronous replication** means the primary database does not consider a write successfully committed until the required replica(s) have also confirmed that the write has been persisted.
**Asynchronous replication**

## Setting up new follower

Simply compying data files from one node to another is typically not sufficient, Clients are constantly writing to the datebase, and the data is always in flux, so a standard file compy would see different parts of the database at different points in time. The result might not make an sense.

You could make the files on disk onsistent by locking the database (making a unavailable for writes), but that would go against our goal of high availablility. **Fortunately, setting up a follower can usually be done without downtime**.

The process:
1. Take a consistent snapshot of the leader's database at some point in time - if possible without locking the entire database. Most database have this feature, as it is also without locking the entire database. Most dataabses have this feature, as it is also required for backups. In some cases, third-party tools are needed, such as Percona XtraBackup for MySQL.
2. Copy the snapshot to the new follower node.
3. The follower connects to the leader and requests all the data changes that have happened since the snapshot was taken. This requires that the snapshot is associated with an exact position in the leader's replication log. That position has various names - for example PostgreSQL calls it the **log sequence number, MySQL** has two mechanisms, **binlog coordinates and Gloabal Transaction Identifiers.**
4. When the follower has processed the backlog of data changes since the snapshot, we say it has caught up. It can now continue to process data changes from the leader as they happen.

"You can also achieve the replication log to an object store along with periodic snapshots of the whole database." This is a good way of implementing database backups and disaster reovery, and you can perform steps 1 and 2 of setting up a new follower by downloading thos files from the obect store.

### How does the follower connects to the leader for the data
**The follower was initialized from a snapshot:**
The key idea is that the follower does not ask the leader, "Give me all changes after this timestamp". It gives the leader a **replication position** representing exactly where the snapshot ends, and asks for chnages after that position.

After restoring the snapshot, the follower connects to the leader and effectively says "I have data through LSN 5000 Send me replication records starting after LSN 5000." The leader then streams and follower applies those changes in order.

The important part is the **replication position**. Different database call it different things:
PostgreSQL: WAL LSN
MySQL: binary-log file + position, or GTID
Kafka: offset
Some distributed database: log index/term/sequence number

> [!NOTE]
> The subtle but critical point is that the leader must retain the replication log from the snapshot position onward. If the snapshot says `5000` but the leader has already discarded WAL/binlog entries `5001-5200`, the follower cannot simply continue. It needs another snapshot/base-backup.

## Handling Node Outages
Any node in the system can go down, perhaps unexpectedly because of a fault, but also because of planned maintenance (e.g., rebooting a machine to install a kernel security patch). Being able to reboot individual nodes without downtime is a big advantage for operations and maintenance. Tus, our goal is to keep the system as a whole running despite individual node failures, and to keep the imparct of a node outage as small as possiblle.

