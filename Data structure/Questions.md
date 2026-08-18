[[Data structure]] [[dsa problem solving Scaffold]] [[dsa intuition]]

# Questions

> DSA question bank mindset — classify the prompt, pick a pattern, then solve with the scaffold.

## Mental model

**Say it in one breath:** Tag each problem (array/string/tree/graph/DP), list constraints, then apply the matching pattern from [[dsa intuition]].

```txt
read → tag → constraints → pattern → code → edges
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Tag** | Topic label | “This is sliding window.” |
| --- | --- | --- |
| **Similar problems** | Transfer learning | “Same as two-sum variant.” |
| **Follow-ups** | Harder constraints | “What if sorted? streamed?” |
| **Complexity ask** | Time/space | “State both.” |

## Standard config / commands

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

| Time box | Don’t sink 40m on one |
| --- | --- |
| Verbalize | Interview signal |
| Postmortem | Note the pattern gap |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Blank stare | no tag | Restate + examples |
| Overengineered | n tiny | Brute is OK |
| Pattern mismatch | wrong family | Re-tag problem |
| Repeat misses | no journal | Log pattern → question |

## Gotchas

> [!WARNING]
> **Collecting solutions without tags** — unsearchable later.

> [!WARNING]
> **Only LeetCode Easy** — medium graph/DP is where interviews live.

## When NOT to use

- **On-call incident** — use runbooks, not puzzle mode.
- **production feature with clear CRUD** — don’t force interview patterns.

## Related

[[dsa problem solving Scaffold]] [[dsa intuition]] [[DSA algorithms]]
