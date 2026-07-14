[[Concurrency]] [[Database]]

OCC (Optimistic Concurrency Control) -> executes transactions across three strictly ordered phases without acquiring exclusive or shared locks on the underlying data records.

Read Phase (Workspace Allocation) -> The transaction reads data from the shared database into a private memory workspace. All state mutations (inserts, updates, deletes) are applied to this local context. The system tracks a Read Set (records read, including their versions/timestamps) and a Write Set (records modified).

Validation Phase (Conflict Detection) -> Prior to commit, the transaction manager verifies that no other committed transaction has mutated the records in the current transaction's Read Set.

- Backward validation: Checks if the Read Set intersects with the Write Sets of transactions that committed after the current transaction started.
- Forward validation: Checks if the Write Set intersects with the Read Sets of active transactions.

Write Phase (Commit/Abort) -> If the validation succeeds, the workspace state is flushed to the durable store. If it fails, the transaction is aborted, rolled back, and typically yields to a retry heuristic.