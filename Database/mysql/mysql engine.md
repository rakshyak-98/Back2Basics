`ENGINE=InnoDB` -> is the default and most advanced storage engine in MySQL, whey you set
```mysql
CREATE TABLE my_table () ENGINE=InnoDB;
```

| Feature                 | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| ✅ **ACID compliant**    | Ensures Atomicity, Consistency, Isolation, Durability (via transactions)  |
| ✅ **Row-level locking** | Better concurrency than table-locking engines                             |
| ✅ **Foreign keys**      | Supports `FOREIGN KEY` constraints                                        |
| ✅ **Crash recovery**    | Uses write-ahead logs to recover safely from crashes                      |
| ✅ **MVCC**              | Multi-Version Concurrency Control — enables non-blocking reads            |
| ✅ **Clustered index**   | Primary key data is physically ordered with the table (performance boost) |

## MySQL storage Engines comparison: `InnoDB` `MyISM` `MEMORY`

|Feature|InnoDB|MyISAM|MEMORY|
|---|---|---|---|
|**Storage**|Disk|Disk|RAM (volatile)|
|**Persistence**|✅ Persistent|✅ Persistent|❌ Lost on restart|
|**Transactions (ACID)**|✅ Yes|❌ No|❌ No|
|**Row-level locking**|✅ Yes|❌ Table-level only|❌ Table-level only|
|**Foreign keys**|✅ Yes|❌ No|❌ No|
|**Crash recovery**|✅ Automatic recovery|❌ Manual repair needed|❌ Data lost|
|**Index type**|`BTREE` (default)|`BTREE`|`HASH` (default), `BTREE` opt|
|**Concurrency**|✅ High (row locks + MVCC)|❌ Poor (full table lock)|⚠️ Limited (RAM-bound)|
|**Full-text search**|✅ Since 5.6|✅ Native support|❌ Not supported|
|**Storage size**|Medium|Smaller|N/A|
|**Use cases**|General-purpose, safe ops|Read-heavy, no transactions|Temp cache/lookups|

`InnoDB` -> use for most production workloads (safety, concurrency, FK).
`MyISAM` -> use for read-heavy, non-critical legacy apps.
`MEMORY` -> use for temporary, fast, non-persistent in-RAM memory.