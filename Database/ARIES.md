[[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[ACID]] [[Database]]

# ARIES

> IBM's Algorithm for Recovery and Isolation Exploiting Semantics—industrial-strength WAL recovery using steal/no-force buffer management, redo, and undo phases keyed by Log Sequence Numbers.

```txt
        ARIES ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** ARIES shows up when reviewers probe crash recovery depth: Analysis → Redo …

## Sources
- Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks" (1992) — deep-dive
- Gray & Reuter, *Transaction Processing: Concepts and Techniques* (1993) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3–5 (logging & recovery context) — overview

## Key Concepts
- **Log Sequence Number (LSN):** monotonic position in the log → pages and transactions track “how far” they a…
- **Steal / no-force:** dirty pages may hit disk before commit
- **Repeat history:** redo replays even aborted transactions’ logged changes → undo then rolls them…
- **Checkpoint:** shortens Analysis/Redo start point → recovery time tracks WAL volume since la…


- **Core:** ARIES is a WAL-based recovery method: after a crash, the system analyzes the …

## Technical Details
- Three phases of crash recovery:

| Phase | Action |
|-------|--------|
| **Analysis** | Scan WAL from last checkpoint; build dirty page table and active transaction table |
| **Redo** | Replay all logged changes from checkpoint—even for aborted transactions (repeat history) |
| **Undo** | Roll back transactions that were active at crash time |

- ARIES assumes **steal** (dirty pages may be written before commit) and **no-f…
- That combination maximizes throughput but **requires** a correct [[WAL (Write…

- PostgreSQL and InnoDB recovery differ in details but share the WAL-first ment…

## Mistakes to Avoid
- **Mistake:** Thinking redo only applies committed transactions
- **Mistake:** Confusing steal/no-force with “no durability”
- **Mistake:** Ignoring checkpoint lag

## Pros/Cons or Trade-offs
- **Pro:** Supports fine-granularity locking, partial rollbacks, and high throughput under steal/no-force.
- **Con:** Recovery cost grows with WAL since checkpoint; incorrect LSN/WAL discipline corrupts the database.

## Comparison
- vs [[ACID]]: ACID states durability/atomicity goals


### Use cases
- Reasoning about why a long recovery follows a crash after a long gap between …
