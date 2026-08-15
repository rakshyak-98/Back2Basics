[[Data structure]] [[ADT (Abstract Data Type)]] [[DSA algorithms]] [[array]] [[linked list]]

# Data structure

> Data structures store data with different access costs — pick for the operations you run most.

## Interview Relevance

Interviewers expect you to pick structures by access pattern and cost — not by name familiarity.

## Sources

- [Wikipedia — Data structure](https://en.wikipedia.org/wiki/Data_structure) — overview
- [MIT 6.006 — Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive

## Key Concepts

```txt
ops you need → structure → complexity tradeoffs
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Access vs update** | Read pattern vs write | “Optimize the hot path.” |
| **Amortized** | Average over ops | “Dynamic array append.” |
| **Locality** | Cache friendliness | “Arrays beat pointer chasing.” |
| **ADT vs impl** | Behavior vs layout | “Queue can be ring buffer.” |

## Technical Details

```text
need O(1) avg lookup     → hash map
need sorted order        → balanced tree / skip list
need min/max fast        → heap
need FIFO                → queue / deque
need relationships       → graph (adj list)
```

| Knob | Why it matters |
|------|----------------|
| Op mix | Wrong structure = death by a thousand cuts |
| Memory | Pointer-heavy structures cost RAM |
| Concurrency | Most classic DS aren’t thread-safe |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Hot loop slow | wrong Big-O | Change structure |
| GC pressure | many tiny nodes | Contiguous arrays |
| Ordering bugs | unstable map iteration | Use ordered structure |
| Memory blow | unbounded cache | Bound + eviction |

## Pros/Cons or Trade-offs

- **Trade-off:** Tiny n — simplest container wins.
- **Trade-off:** When a database index already solves it — don’t rebuild in application memory casually.

## Mistakes to Avoid

- Premature cleverness — array + scan beats fancy trees at small n.
- Language defaults — “list” in Python is array; LinkedList in Java is nodes.
