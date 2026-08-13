[[ML]] [[prompt]] [[prompt enginerring]] [[claude ai]]

# GPT

> GPT-style models predict the next token — chat APIs wrap that into messages, tools, and completions.

---

## How it works

```txt
messages[] → API → assistant tokens (+ optional tool_calls)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Tokens** | Chunks of text | “Cost and context are token-based.” |
| **Context window** | Max tokens in play | “Truncate or summarize history.” |
| **Temperature** | Randomness | “0 for extractive tasks.” |
| **Tool/function call** | Structured side effect | “Model proposes; app executes.” |

---


## Configuration and commands

```python
# sketch
client.chat.completions.create(
  model='gpt-4.1-mini',
  temperature=0,
  messages=[
    {'role': 'system', 'content': 'Be concise.'},
    {'role': 'user', 'content': question},
  ],
)
```

| Knob | Why it matters |
|------|----------------|
| Model choice | Quality/cost/latency |
| `response_format` | JSON mode |
| Seed (when available) | Repro experiments |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Context exceeded | token count | Trim history; summarize |
| 429 rate limit | headers | Backoff; smaller prompts |
| Unstable JSON | free-form | schema / JSON mode |
| Stale answers | no tools/RAG | Ground with retrieval |

---


## Gotchas

> [!WARNING]
> **Training cutoff** — doesn’t know your private docs unless you pass them.

> [!WARNING]
> **Confident wrong** — verify critical facts outside the model.

---


## When not to use

- **Strict deterministic logic** — write code.
- **Tiny classify with tons of labels** — classical model may win.


## Related

[[prompt enginerring]] [[claude ai]] [[prompt]]

## Sources

- [Wikipedia — GPT](https://en.wikipedia.org/wiki/GPT)
