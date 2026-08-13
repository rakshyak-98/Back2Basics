<!-- note-strategy: operational -->
[[ML]] [[prompt enginerring]] [[GPT]] [[claude ai]]

# prompt

> A prompt is the input text/messages you send an LLM — instructions plus the user ask.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Clear task + constraints + context beats clever wording; treat prompts as versioned configuration.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Ignores rules | buried instruction | Repeat constraints; system role |
| Uses outside knowledge | no grounding rule | “only Context” + refuse |
| Unstable | vague ask | Examples + schema |
| Injection | user overrides system | Delimit; strip instructions |

---

## Gotchas

> [!WARNING]
> **Prompts in code without tests** — silent quality regressions.

> [!WARNING]
> **Pasting secrets into prompts** — they may be logged by the provider.

---

## When NOT to use

- **Deterministic transforms** — regex/code.
- **Private data you can’t send off-box** — local models or classical pipelines.

## Related

[[prompt enginerring]] [[GPT]] [[claude ai]]
