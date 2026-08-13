[[ML]] [[prompt]] [[GPT]] [[claude ai]]

# prompt enginerring

> Prompt engineering shapes LLM behavior with instructions, examples, and structure — not weight updates.

---

## How it works

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


## Configuration and commands

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


## When things break

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


## When not to use

- **Stable classify/extract at scale** — fine-tune or classical ML may be cheaper.
- **Hard guarantees** — code + tests, not prose prompts alone.


## Related

[[prompt]] [[GPT]] [[claude ai]]

## Sources

- [Wikipedia — prompt enginerring](https://en.wikipedia.org/wiki/prompt_enginerring)
