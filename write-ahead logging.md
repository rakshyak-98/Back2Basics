WAL
- Append only auxiliary disk-resident structure used for crash and transaction recovery.
- the changes are first recorded in the log, which must be written to the stable storage, before the changes are written to the database.
- every operation that modifies the database state has to be logged on disk before the contents on the associated pages can be modified.
- allow lost in-memory changes to be reconstructed from the operation log in case of crash.