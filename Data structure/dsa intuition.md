[[Data structure]] [[dsa problem solving Scaffold]] [[DSA algorithms]] [[algo/Two pointer]] [[sliding window]] [[algo/greedy algorithm]]

# dsa intuition

> DSA intuition is recognizing which pattern fits — before you write a line of code.





## Interview Relevance
Pattern intuition is the soft skill behind DSA interviews — classify before coding, then justify complexity.

## Sources
- [NeetCode — Pattern roadmap](https://neetcode.io/roadmap) — overview
- [MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive

## Key Concepts
```txt
clue → pattern → structure → prove → code
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Subarray / window** | Contiguous | Sliding window / prefix |
| **Subsequence** | Not contiguous | DP / two pointers |
| **Shortest / levels** | Graph distance | BFS |
| **Optimal substructure** | DP | “State + transition.” |
| **Greedy choice** | Local → global | Prove exchange argument |

## Technical Details
```text
sorted + pairs           → two pointers / binary search
contiguous sum/len       → sliding window / prefix
parent/child relations   → tree DFS/BFS
dependencies             → topo sort
count ways / max score   → DP
```

| Knob | Why it matters |
|------|----------------|
| Contiguous? | Window vs subsequence |
| Weights? | BFS vs Dijkstra |
| Overlapping subproblems | DP vs plain recursion |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong pattern | re-read clues | Contiguous? ordered? graph? |
| DP explosion | state too big | Compress / greedy if valid |
| BFS TLE | branching | Visited set; better model |
| Greedy WA | no proof | Fall back to DP |

## Pros/Cons or Trade-offs
- **Trade-off:** Systems design interviews — different intuition.
- **Trade-off:** When the API already sorts/searches — use the library.

## Mistakes to Avoid
- Forcing DP everywhere — many problems are two pointers + sort.
- Ignoring “contiguous” — the whole game for windows.
