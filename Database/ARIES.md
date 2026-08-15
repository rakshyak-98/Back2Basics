[[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[ACID]] [[Database]]

# ARIES

> IBM's Algorithm for Recovery and Isolation Exploiting Semantics—industrial-strength WAL recovery using steal/no-force buffer management, redo, and undo phases keyed by Log Sequence Numbers.

## Interview Relevance

ARIES shows up when interviewers probe crash recovery depth: Analysis → Redo → Undo, steal/no-force, and why repeating history (redo aborted txs then undo) is correct. Understanding ARIES clarifies checkpoints, recovery time, and why [[WAL (Write-Ahead Log)]] must precede page writes.

## Sources

- Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks" (1992) — deep-dive
- Gray & Reuter, *Transaction Processing: Concepts and Techniques* (1993) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3–5 (logging & recovery context) — overview

## Core Definition

ARIES is a WAL-based recovery method: after a crash, the system analyzes the log from the last checkpoint, redos all logged changes (repeat history), then undoes transactions that were still active at crash time.

## Key Concepts

- **Log Sequence Number (LSN):** monotonic position in the log → pages and transactions track “how far” they are recovered.
- **Steal / no-force:** dirty pages may hit disk before commit; committed pages need not flush before commit → high throughput, requires correct WAL.
- **Repeat history:** redo replays even aborted transactions’ logged changes → undo then rolls them back cleanly.
- **Checkpoint:** shortens Analysis/Redo start point → recovery time tracks WAL volume since last checkpoint.

## Technical Details

Three phases of crash recovery:

| Phase | Action |
|-------|--------|
| **Analysis** | Scan WAL from last checkpoint; build dirty page table and active transaction table |
| **Redo** | Replay all logged changes from checkpoint—even for aborted transactions (repeat history) |
| **Undo** | Roll back transactions that were active at crash time |

ARIES assumes **steal** (dirty pages may be written before commit) and **no-force** (committed pages need not be flushed before commit). That combination maximizes throughput but **requires** a correct [[WAL (Write-Ahead Log)]].

PostgreSQL and InnoDB recovery differ in details but share the WAL-first mental model ARIES popularized.

## Real-World Applications

Reasoning about why a long recovery follows a crash after a long gap between checkpoints, or why turning off sync commits risks acknowledged-but-lost transactions. Example: ops increases checkpoint frequency before a planned failover to bound redo time.

## Pros/Cons or Trade-offs

- **Pro:** Supports fine-granularity locking, partial rollbacks, and high throughput under steal/no-force.
- **Con:** Recovery cost grows with WAL since checkpoint; incorrect LSN/WAL discipline corrupts the database.

## Comparison

vs [[ACID]]: ACID states durability/atomicity goals; ARIES is one industrial algorithm that implements them via WAL. vs [[write-ahead logging]]: WAL is the mechanism; ARIES specifies Analysis/Redo/Undo over that log.

## Mistakes to Avoid

- Thinking redo only applies committed transactions — ARIES redos history, then undoes losers.
- Confusing steal/no-force with “no durability” — durability still requires WAL flush before commit acknowledgment.
- Ignoring checkpoint lag — recovery time is dominated by redo volume, not table size alone.
