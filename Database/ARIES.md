[[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[ACID]] [[Database]]

# ARIES

> IBM's Algorithm for Recovery and Isolation Exploiting Semantics—industrial-strength WAL recovery using steal/no-force buffer management, redo, and undo phases keyed by Log Sequence Numbers.

## Three phases of crash recovery

| Phase | Action |
|-------|--------|
| **Analysis** | Scan WAL from last checkpoint; build dirty page table and active transaction table |
| **Redo** | Replay all logged changes from checkpoint—even for aborted transactions (repeat history) |
| **Undo** | Roll back transactions that were active at crash time |

## Steal and no-force

ARIES assumes **steal** (dirty pages may be written before commit) and **no-force** (committed pages need not be flushed before commit). That combination maximizes throughput but **requires** a correct [[WAL (Write-Ahead Log)]].

## Influence

PostgreSQL and InnoDB recovery differ in details but share the WAL-first mental model ARIES popularized. Understanding ARIES clarifies why logs grow, why checkpoints matter, and why recovery time depends on WAL volume since the last checkpoint.

## Sources

- Mohan, C., Haderle, D., Lindsay, B., Pirahesh, H., Schwarz, P., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks" (1992)
- Gray & Reuter, *Transaction Processing: Concepts and Techniques* (1993)
