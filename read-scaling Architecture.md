increasing the read-only replica by adding more followers. This approach realistically works only with asynchronous replication.
If you tried to synchronously replicate to all followers, a single node failure or network outage would make the entire system unavailable for writing.

Unfortunately, an application reading from an *asynchronous follower* may see outdated information if the follower has fallen behind. This leads to apparent inconsistencies in the databases; if you run the same query on the leader and follower at the same time, you may get different results, because not all writes have been reflected in the follower. This inconsistency is a temporary state - if you stop writing to the database and wait a while, the followers will eventually catch up and become consistent with the leader. For that reason, this effect is know as **eventual consistency.**

**How does read follower replica are being update?**
A read replica is not updated by copying the whole database every time a write happens. The primary database records the changes in a **replication log,** and the replica continuously receives and applies those changes.