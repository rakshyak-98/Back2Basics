[[ML]] [[prompt enginerring]] [[GPT]] [[claude ai]]

# prompt

> A prompt is the input text/messages you send an LLM — instructions plus the user ask.

---

## How it works

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


## Configuration and commands

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


## When things break

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


## When not to use

- **Deterministic transforms** — regex/code.
- **Private data you can’t send off-box** — local models or classical pipelines.


## Related

[[prompt enginerring]] [[GPT]] [[claude ai]]

## Sources

- [Wikipedia — prompt](https://en.wikipedia.org/wiki/prompt)
