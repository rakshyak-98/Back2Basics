[[Data structure]] [[dsa problem solving Scaffold]] [[dsa intuition]] [[DSA algorithms]]

# Questions

> DSA question bank mindset — classify the prompt, pick a pattern, then solve with the scaffold.

```txt
        Questions ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Question-bank discipline

## Sources
- [NeetCode roadmap](https://neetcode.io/roadmap) — overview
- [LeetCode Explore](https://leetcode.com/explore/) — overview

## Key Concepts
```txt
read → tag → constraints → pattern → code → edges
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Tag** | Topic label | “This is sliding window.” |
| **Similar problems** | Transfer learning | “Same as two-sum variant.” |
| **Follow-ups** | Harder constraints | “What if sorted? streamed?” |
| **Complexity ask** | Time/space | “State both.” |

## Technical Details
```text
Checklist per question:
[ ] I/O + constraints
[ ] 3 examples (incl empty)
[ ] Brute complexity
[ ] Target complexity
[ ] Pattern name
[ ] Edge cases tested
```

| Knob | Why it matters |
|------|----------------|
| Time box | Don’t sink 40m on one |
| Verbalize | Review signal |
| Postmortem | Note the pattern gap |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank stare | no tag | Restate + examples |
| Overengineered | n tiny | Brute is OK |
| Pattern mismatch | wrong family | Re-tag problem |
| Repeat misses | no journal | Log pattern → question |

## Mistakes to Avoid
- **Mistake:** Collecting solutions without tags — unsearchable later
- **Mistake:** Only LeetCode Easy — medium graph/DP is where reviews live

## Pros/Cons or Trade-offs
- **Trade-off:** On-call incident — use runbooks, not puzzle mode.
- **Trade-off:** production feature with clear CRUD — don’t force review patterns.
