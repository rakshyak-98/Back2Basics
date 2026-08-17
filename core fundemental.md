[[Data structure/Data structure]] [[Operating System]] [[Networking]] [[Database]] [[staff engineer]] [[INDEX]]

# core fundemental

> Core computer-science fundamentals — the durable mental models behind every stack: algorithms, systems, networks, and data.

```txt
        core fundemental ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Staff and senior interviews still probe these foundations

## Sources
- [MIT OpenCourseWare — Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive
- [Stanford CS144 — Computer Networks](https://cs144.github.io/) — overview
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — deep-dive

## Key Concepts
- **Algorithms & DS:** Sorting, searching, hashing, trees/graphs, complexity ([[Data structure/Data …
- **Systems:** Processes/threads, virtual memory, scheduling, I/O, locks ([[Operating System…
- **Networking:** Layers, TCP vs UDP, DNS, TLS, latency vs bandwidth ([[Networking]]).
- **Data:** Transactions, indexes, replication, consistency models ([[Database]], [[ACID]…
- **Engineering practice:** Testing, observability, [[Release cycle]], security basics.


- **Core:** “Core fundamentals” are the ideas that outlive languages: how to organize dat…

## Technical Details
- Checklist (study, do not memorize as trivia):

| Area | Must be able to explain |
|------|-------------------------|
| Algorithms | Big-O of common sorts/searches; hash collision handling |
| Memory | Stack vs heap; cache locality; GC vs manual |
| Concurrency | Race, deadlock, happens-before; when to use queues |
| Networks | Handshake, retransmission, head-of-line; TLS role |
| Storage | WAL/fsync intuition; index vs full scan |
| Reliability | Idempotency, timeouts, retries with backoff |

## Mistakes to Avoid
- **Mistake:** Treating this note as a complete curriculum
- **Mistake:** Reciting definitions without complexity or failure trade-offs
- **Mistake:** Skipping hands-on: implement one sort, one lock bug, one TCP cap…

## Pros/Cons or Trade-offs
- **Pro:** Transferable across decades of tooling; improves debugging speed.
- **Con:** Easy to over-study theory without shipping; balance with deliberate practice on real systems.

## Comparison
- vs framework knowledge: frameworks change yearly


### Use cases
- Outage: “API slow.” Fundamentals path
