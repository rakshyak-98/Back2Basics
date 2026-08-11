[[Data structure]] [[dsa problem solving Scaffold]] [[DSA algorithms]]

# dsa intuition

> DSA intuition is recognizing which pattern fits — before you write a line of code.

---

## Mental model

**Say it in one breath:** Hear the clue words (“subarray”, “shortest”, “combinations”) and map them to a technique.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong pattern | re-read clues | Contiguous? ordered? graph? |
| DP explosion | state too big | Compress / greedy if valid |
| BFS TLE | branching | Visited set; better model |
| Greedy WA | no proof | Fall back to DP |

---

## Gotchas

> [!WARNING]
> **Forcing DP everywhere** — many problems are two pointers + sort.

> [!WARNING]
> **Ignoring “contiguous”** — the whole game for windows.

---

## When NOT to use

- **Systems design interviews** — different intuition.
- **When the API already sorts/searches** — use the library.

## Related

[[dsa problem solving Scaffold]] [[algo/Two pointer]] [[sliding window]] [[algo/greedy algorithm]]
