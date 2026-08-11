[[Data structure]] [[ADT (Abstract Data Type)]] [[DSA algorithms]]

# Data structure

> Data structures store data with different access costs — pick for the operations you run most.

---

## Mental model

**Say it in one breath:** Arrays for index access, hash maps for keyed lookup, trees/heaps for ordered extremes, graphs for relationships.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hot loop slow | wrong Big-O | Change structure |
| GC pressure | many tiny nodes | Contiguous arrays |
| Ordering bugs | unstable map iteration | Use ordered structure |
| Memory blow | unbounded cache | Bound + eviction |

---

## Gotchas

> [!WARNING]
> **Premature cleverness** — array + scan beats fancy trees at small n.

> [!WARNING]
> **Language defaults** — “list” in Python is array; LinkedList in Java is nodes.

---

## When NOT to use

- **Tiny n** — simplest container wins.
- **When a database index already solves it** — don’t rebuild in application memory casually.

## Related

[[ADT (Abstract Data Type)]] [[array]] [[linked list]] [[DSA algorithms]]
