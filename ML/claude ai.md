<!-- note-strategy: operational -->
[[ML]] [[prompt]] [[GPT]] [[prompt enginerring]]

# claude ai

> Claude is Anthropic’s chat/tool model — same message loop as other LLMs, strict about `tool_use` ↔ `tool_result` pairing.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Send messages; if Claude returns `tool_use`, your next message must include matching `tool_result` blocks immediately after.

```txt
user → assistant (tool_use) → user (tool_result) → assistant (answer)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **tool_use** | Model requests a tool | “Must pair with tool_result.” |
| **tool_result** | Your execution output | “Same id as tool_use.” |
| **Rate limit** | Tokens per minute | “Backoff; shrink context.” |
| **Messages API** | Official shape | “Roles + content blocks.” |

---

## Standard config / commands

```text
# Fix tool pairing
messages[n]   assistant: tool_use id=toolu_123
messages[n+1] user:      tool_result tool_use_id=toolu_123  ← required next
```

| Knob | Why it matters |
|------|----------------|
| Max tokens | Avoid truncated tool JSON |
| Cache / prompt size | Cost and rate limits |
| Idempotent tools | Safe retries on 429 |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| tool_use without tool_result | message order | Insert results before next call |
| 429 rate_limit_error | TPM headers | Backoff; shorten prompts |
| 400 invalid_request | schema/content blocks | Match API content types |
| Empty assistant | max_tokens too low | Raise limit |

---

## Gotchas

> [!WARNING]
> **Dropping tool_results when “simplifying” history** — Claude 400s on orphan tool_use ids.

> [!WARNING]
> **Retrying the whole transcript after a partial tool** — can double side effects; make tools idempotent.

---

## When NOT to use

- **No-tool plain completion** — still fine; just don’t half-implement tools.
- **Hard realtime <100ms** — LLMs aren’t that path.

## Related

[[prompt enginerring]] [[GPT]] [[prompt]]
