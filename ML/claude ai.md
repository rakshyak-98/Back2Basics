[[ML]] [[prompt]] [[GPT]] [[prompt enginerring]]

# claude ai

> Claude is Anthropic’s chat/tool model — same message loop as other LLMs, strict about `tool_use` ↔ `tool_result` pairing.

```txt
        claude ai ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about claude ai to check whether you can choose models/metri…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
```txt
- **Note:** user → assistant (tool_use) → user (tool_result) → assistant (answer)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **tool_use** | Model requests a tool | “Must pair with tool_result.” |
| **tool_result** | Your execution output | “Same id as tool_use.” |
| **Rate limit** | Tokens per minute | “Backoff; shrink context.” |
| **Messages API** | Official shape | “Roles + content blocks.” |

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Dropping tool_results when “simplifying” history** — Claude 400s on orphan tool_use ids.

> [!WARNING]
> **Retrying the whole transcript after a partial tool** — can double side effects; make tools idempotent.

| Symptom | Check | Fix |
|---------|-------|-----|
| tool_use without tool_result | message order | Insert results before next call |
| 429 rate_limit_error | TPM headers | Backoff; shorten prompts |
| 400 invalid_request | schema/content blocks | Match API content types |
| Empty assistant | max_tokens too low | Raise limit |

## Pros/Cons or Trade-offs
- **No-tool plain completion** — still fine; just don’t half-implement tools.
- **Hard realtime <100ms** — LLMs aren’t that path.
