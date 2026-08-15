[[Data structure]] [[dsa problem solving Scaffold]] [[dsa intuition]] [[DSA algorithms]]

# Questions

> DSA question bank mindset — classify the prompt, pick a pattern, then solve with the scaffold.

## Interview Relevance

Question-bank discipline — tagging, constraints, follow-ups — is how strong candidates stay structured under pressure.

## Sources

- [NeetCode roadmap](https://neetcode.io/roadmap) — overview
- [LeetCode Explore](https://leetcode.com/explore/) — overview

## Key Concepts

```txt
read → tag → constraints → pattern → code → edges
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
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
| Verbalize | Interview signal |
| Postmortem | Note the pattern gap |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank stare | no tag | Restate + examples |
| Overengineered | n tiny | Brute is OK |
| Pattern mismatch | wrong family | Re-tag problem |
| Repeat misses | no journal | Log pattern → question |

## Pros/Cons or Trade-offs

- **Trade-off:** On-call incident — use runbooks, not puzzle mode.
- **Trade-off:** production feature with clear CRUD — don’t force interview patterns.

## Mistakes to Avoid

- Collecting solutions without tags — unsearchable later.
- Only LeetCode Easy — medium graph/DP is where interviews live.
