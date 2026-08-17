[[ML]] [[prompt enginerring]] [[GPT]] [[claude ai]]

# prompt

> A prompt is the input text/messages you send an LLM — instructions plus the user ask.

```txt
        prompt ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about prompt to check whether you can choose models/metrics …

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
```txt
[system rules] + [context] + [user task] → model → output
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Instruction** | What to do | “Summarize in 3 bullets.” |
| **Context** | Facts to use | “Paste retrieved docs.” |
| **Delimiter** | Fence untrusted text | “XML/JSON wrappers.” |
| **Template** | Reusable prompt | “Fill slots; don’t freestyle.” |

## Technical Details
```text
### Context
{{docs}}
### Task
Answer using only Context. If missing, say "unknown".
### Answer
```

| Knob | Why it matters |
|------|----------------|
| Version id | Rollback bad prompts |
| Eval set | Catch regressions |
| Length | Cost + attention |

## Mistakes to Avoid
> [!WARNING]
> **Prompts in code without tests** — silent quality regressions.

> [!WARNING]
> **Pasting secrets into prompts** — they may be logged by the provider.

| Symptom | Check | Fix |
|---------|-------|-----|
| Ignores rules | buried instruction | Repeat constraints; system role |
| Uses outside knowledge | no grounding rule | “only Context” + refuse |
| Unstable | vague ask | Examples + schema |
| Injection | user overrides system | Delimit; strip instructions |

## Pros/Cons or Trade-offs
- **Deterministic transforms** — regex/code.
- **Private data you can’t send off-box** — local models or classical pipelines.
