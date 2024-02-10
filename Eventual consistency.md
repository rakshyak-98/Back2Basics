is a consistency model used in [[Distributed computing]] to achieve high availability that informally guarantees
- new updates are made to a given data item, all accesses to that item will return the last updated value.
- Eventual consistency, also called *optimistic replication*
- weak guarantee
Most stronger models, like [[linerizability]] are trivially eventually consistent.
## BASE
Basically-Available Soft-state Eventual consistency
### Basically available
- reading and writing operations are available as much as possible (using all nodes of databases cluster)
- might not be consistent (the write might not persist after conflict are reconciled, and the read might not get the latest write).
### Soft-state
- without consistency guarantees, after some amount of time, we only have some probability of knowing the state, since it might not yet have converged (to tend to meet in a point of line).
### Eventually consistent
- if we execute some writes and then the system functions long enough, we can know the state of the data, any further reads of the data item will return the same value.
> [!NOTE] Eventually consistent
> Eventual consistency is sometimes criticised as increasing the complexity of distributed software applications. An eventually consistent system can return any value before it converges.

## Conflict resolution
- ensure replica convergence, must reconcile differences between multiple copies of distributed data.
1. exchanging versions or updates of data between servers (anti-entropy)
2. choosing an appropriate final state when concurrent updates have occurred (reconciliation).
- A widespread approach is "Last writes wins"
- another is invoke a user-specified handler.
- Timestamps and [vector clocks](#vecrot clocks) are often used to detect concurrency between updates.