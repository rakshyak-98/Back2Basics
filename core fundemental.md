[[Data structure/Data structure]] [[Operating System]] [[Networking]] [[Database]] [[staff engineer]] [[INDEX]]

# core fundemental

> Core computer-science fundamentals — the durable mental models behind every stack: algorithms, systems, networks, and data.

## Interview Relevance
Staff and senior interviews still probe these foundations. Interviewers want proof you can reason from first principles when the framework docs run out — complexity, memory, concurrency, and failure.

## Sources
- [MIT OpenCourseWare — Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive
- [Stanford CS144 — Computer Networks](https://cs144.github.io/) — overview
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — deep-dive

## Core Definition
“Core fundamentals” are the ideas that outlive languages: how to organize data, schedule work, move bits, store durable state, and reason about correctness under failure.

## Key Concepts
- **Algorithms & DS:** Sorting, searching, hashing, trees/graphs, complexity ([[Data structure/Data structure]]).
- **Systems:** Processes/threads, virtual memory, scheduling, I/O, locks ([[Operating System]], [[Linux]]).
- **Networking:** Layers, TCP vs UDP, DNS, TLS, latency vs bandwidth ([[Networking]]).
- **Data:** Transactions, indexes, replication, consistency models ([[Database]], [[ACID]]).
- **Engineering practice:** Testing, observability, [[Release cycle]], security basics.

## Technical Details
Checklist (study, do not memorize as trivia):

| Area | Must be able to explain |
|------|-------------------------|
| Algorithms | Big-O of common sorts/searches; hash collision handling |
| Memory | Stack vs heap; cache locality; GC vs manual |
| Concurrency | Race, deadlock, happens-before; when to use queues |
| Networks | Handshake, retransmission, head-of-line; TLS role |
| Storage | WAL/fsync intuition; index vs full scan |
| Reliability | Idempotency, timeouts, retries with backoff |

## Real-World Applications
Outage: “API slow.” Fundamentals path — lock contention? N+1 queries? TCP retransmits? GC thrash? — beats guessing a random Kubernetes knob first.

## Pros/Cons or Trade-offs
- **Pro:** Transferable across decades of tooling; improves debugging speed.
- **Con:** Easy to over-study theory without shipping; balance with deliberate practice on real systems.

## Comparison
vs framework knowledge: frameworks change yearly; fundamentals explain *why* the framework’s defaults exist. Related career model: [[staff engineer]]. Routing: [[INDEX]].

## Mistakes to Avoid
- Treating this note as a complete curriculum — use it as a map into leaf notes.
- Reciting definitions without complexity or failure trade-offs.
- Skipping hands-on: implement one sort, one lock bug, one TCP capture.
