[[GPT]] [[prompt]] [[prompt enginerring]] [[scikitlearn]]

# AI chat with memory

> LLMs are stateless per request — "memory" is **context you re-inject** each turn (history, summaries, RAG chunks) — **OpenAI / Anthropic API docs**.

---

## Mental model

The model does not persist anything between HTTP calls. Every turn you send:

```txt
system prompt + retrieved docs + summarized history + latest user message → model → reply
```

Token budget is finite (`context window`). Long chats hit **context rot** (early facts dropped) and **cost/latency** scale with history length.

| Layer | What it stores | Tradeoff |
|-------|----------------|----------|
| **Full transcript** | Every message in context | Simple; dies at ~128k tokens |
| **Rolling window** | Last N turns | Cheap; forgets old facts |
| **Summary memory** | LLM-compressed history | Keeps themes; loses exact quotes |
| **Vector RAG** | Embeddings of docs + past turns | Scales knowledge; retrieval quality matters |
| **Structured memory** | DB rows (user prefs, facts) | Deterministic; needs schema + extraction |

---

## Standard config / commands

### Minimal chat loop (OpenAI-style)

```python
messages = [
    {"role": "system", "content": "You are a support agent. Use only provided facts."},
]

def chat(user_text: str) -> str:
    messages.append({"role": "user", "content": user_text})
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply
```

### Production pattern: window + summary

```python
MAX_TURNS = 20

def trim(messages):
    system = [m for m in messages if m["role"] == "system"]
    rest = [m for m in messages if m["role"] != "system"]
    if len(rest) > MAX_TURNS * 2:
        # Summarize oldest half, replace with one assistant summary block
        rest = summarize_and_compress(rest)
    return system + rest
```

### RAG memory (retrieve, don't stuff everything)

```python
chunks = vector_store.similarity_search(user_text, k=5)
context = "\n".join(c.page_content for c in chunks)
messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_text}"})
```

Annotate **why**: system prompt sets behavior; RAG grounds facts; trimming protects latency and cost.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Model "forgets" earlier facts | Token count / window size | Summary memory, RAG, or structured DB facts |
| Wrong answers despite docs | Retrieval (`k`, chunk size, embedding model) | Re-chunk, hybrid search, cite sources in prompt |
| Cost spike | Messages array growth | Hard cap turns; summarize; cache embeddings |
| Duplicate / contradictory replies | Multiple memory sources unsynced | Single source of truth; version user profile row |
| PII in logs | What you persist | Redact before store; TTL on conversation tables |

---

## Gotchas

> [!WARNING]
> **Storing full chat in the client** — anyone can tamper with "memory." Treat client history as UX only; authoritative memory lives server-side with user/session ID.

> [!WARNING]
> **Injecting untrusted retrieved text** — RAG chunks can contain prompt-injection strings. Sanitize, attribute, and instruct the model to ignore instructions inside documents.

---

## When NOT to use

- **Single-shot Q&A** with no follow-up — skip memory infrastructure entirely.
- **Strict audit trail required** — prefer structured DB fields over LLM summaries you cannot replay verbatim.
- **Real-time collaborative editing** — use CRDT/OT, not chat history as state.

---

## Related

[[GPT]] · [[prompt enginerring]] · [[ANN]] · [[data preprocessing]]
