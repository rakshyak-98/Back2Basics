<!-- note-strategy: operational -->
[[ML]] [[prompt]] [[GPT]] [[claude ai]]

# prompt enginerring

> Prompt engineering shapes LLM behavior with instructions, examples, and structure — not weight updates.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Say the role, task, constraints, and output format; add few-shot examples when words aren’t enough.

```txt
system/role → task → constraints → format → (examples) → user input
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **System prompt** | Standing rules | “Safety + persona.” |
| **Few-shot** | Show examples | “Teach the pattern.” |
| **Structured out** | JSON / schema | “Parse reliably.” |
| **Tool use** | Call functions | “Model picks tools; you execute.” |

---

## Standard config / commands

```text
You are a senior SRE. Answer with: (1) cause (2) check (3) fix.
Return JSON: {"cause":"","check":"","fix":""}
```

| Knob | Why it matters |
|------|----------------|
| Temperature | Creativity vs determinism |
| Max tokens | Cost / cutoff |
| Schema validation | Catch bad JSON |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Ignores format | weak instruction | Show example JSON; validate |
| Hallucinated facts | no grounding | RAG / tools; say “unknown” |
| Inconsistent | high temperature | Lower temp; tighten system |
| Prompt injection | user controls instruction | Delimit untrusted input |

---

## Gotchas

> [!WARNING]
> **Long prompts ≠ better** — bury the ask; put constraints near the end too.

> [!WARNING]
> **Eval by vibes** — keep a golden set of prompts/tests.

---

## When NOT to use

- **Stable classify/extract at scale** — fine-tune or classical ML may be cheaper.
- **Hard guarantees** — code + tests, not prose prompts alone.

## Related

[[prompt]] [[GPT]] [[claude ai]]
