Two-Phase Commit (2PC) is a distributed transaction protocol used when **one logical transaction must update multiple independent systems/databases atomically.**

> Either every participant commits, or every participant rolls back.

This is you don't want to happen, instead of doing this 2PC introduces a **coordinator** that controls the transaction.
```txt
Bank A -> Commit
Bank B -> Rollback
````

Each database does the work required to make the transaction commit-able, but **does not commit yet.**

```sql
BEGIN;

UPDATE account SET balance = balance-1000
WHERE id = 'A';

-- Ready to commit, but not committed yet.
```

```txt
			 ┌──────────────┐
			 │ Coordinator  │
			 └──────┬───────┘
							│
			 PHASE 1: PREPARE
							│
		┌─────────┴─────────┐
		▼                   ▼
	DB A                 DB B
 PREPARE              PREPARE
		│                   │
		└─────────┬─────────┘
							│
				Everyone YES?
					 /       \
				 YES        NO
					│          │
	PHASE 2: COMMIT   ABORT
					│          │
		┌─────┴─────┐    │
		▼           ▼    ▼
	DB A         DB B  ROLLBACK
 COMMIT       COMMIT
```

The "prepare" phase exists: This is the important part.
If the coordinator immediately told DB A to commit, you'd have:
```txt
DB A -> Commited
DB B -> unavailable
```
The transaction cannot be safely completed.

**With 2PC, DA A first says**
"I've done the work and I'm ready. I won't commit until you tell me."
Only after **all participants are prepared** does the coordinator issue the final commit.

> The 2PC have to **hold/ locks/resources while waiting for the coordinator to recover.**

