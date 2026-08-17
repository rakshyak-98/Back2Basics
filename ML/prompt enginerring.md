[[ML]] [[prompt]] [[GPT]] [[claude ai]]

# prompt enginerring

> Prompt engineering shapes LLM inputs so outputs are reliable, constrained, and useful for a task.

```txt
        prompt enginerring ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Prompt engineering interviews cover constraints, few-shot examples, and evalu…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
```txt
- **Note:** system/role → task → constraints → format → (examples) → user input
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **System prompt** | Standing rules | “Safety + persona.” |
| **Few-shot** | Show examples | “Teach the pattern.” |
| **Structured out** | JSON / schema | “Parse reliably.” |
| **Tool use** | Call functions | “Model picks tools; you execute.” |

## Technical Details
```text
You are a senior SRE. Answer with: (1) cause (2) check (3) fix.
Return JSON: {"cause":"","check":"","fix":""}
```

| Knob | Why it matters |
|------|----------------|
| Temperature | Creativity vs determinism |
| Max tokens | Cost / cutoff |
| Schema validation | Catch bad JSON |

## Mistakes to Avoid
> [!WARNING]
> **Long prompts ≠ better** — bury the ask; put constraints near the end too.

> [!WARNING]
> **Eval by vibes** — keep a golden set of prompts/tests.

| Symptom | Check | Fix |
|---------|-------|-----|
| Ignores format | weak instruction | Show example JSON; validate |
| Hallucinated facts | no grounding | RAG / tools; say “unknown” |
| Inconsistent | high temperature | Lower temp; tighten system |
| Prompt injection | user controls instruction | Delimit untrusted input |

## Pros/Cons or Trade-offs
- **Stable classify/extract at scale**
- **Hard guarantees** — code + tests, not prose prompts alone.
