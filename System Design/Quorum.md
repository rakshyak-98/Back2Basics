A Quorum is simply the minimum number of nodes that must agree for an operation (read or write) to be considered valid.

> [!NOTE]
> When quorum is lost, the system goes unavailable, but the data is not lost. The surviving nodes still hold it. Once nodes recover, the system comes back up with all data intact.
> - This is the tradeoff -> sacrifice availability to protect data integrity.

### In Distributed Systems

Say you have 5 nodes storing the same data. You set:
- W = 3 -> a write must be confirmed by at least 3 nodes
- R = 3 -> a read must be confirmed by at least 3 nodes

Now if 2 nodes die, you still have 3 alive → writes and reads still work, and no data is lost.

Node 1 ✅  ← has the data
Node 2 ✅  ← has the data
Node 3 ✅  ← has the data
Node 4 💀  ← dead
Node 5 💀  ← dead

Quorum = 3/5 → still reachable → system works fine