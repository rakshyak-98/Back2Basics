[[GPT]] [[prompt]] [[prompt enginerring]] [[scikitlearn]] [[ANN]] [[data preprocessing]]

# AI chat with memory

> AI chat with memory — the model does not persist anything between HTTP calls. Every turn you send:

```txt
        AI chat with memor ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers ask about AI chat with memory to check whether you can choose mo…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
- **Note:** The model does not persist anything between HTTP calls. Every turn you send:

```txt
- **Note:** system prompt + retrieved docs + summarized history + latest user message → m…
```

- **Note:** Token budget is finite (`context window`)

| Layer | What it stores | Tradeoff |
|-------|----------------|----------|
| **Full transcript** | Every message in context | Simple; dies at ~128k tokens |
| **Rolling window** | Last N turns | Cheap; forgets old facts |
| **Summary memory** | LLM-compressed history | Keeps themes; loses exact quotes |
| **Vector RAG** | Embeddings of docs + past turns | Scales knowledge; retrieval quality matters |
| **Structured memory** | DB rows (user prefs, facts) | Deterministic; needs schema + extraction |

## Technical Details
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

- Annotate **why**: system prompt sets behavior

## Mistakes to Avoid
> [!WARNING]
> **Storing full chat in the client** — anyone can tamper with "memory." Treat client history as UX only; authoritative memory lives server-side with user/session ID.

> [!WARNING]
> **Injecting untrusted retrieved text** — RAG chunks can contain prompt-injection strings. Sanitize, attribute, and instruct the model to ignore instructions inside documents.

| Symptom | Check | Fix |
|---------|-------|-----|
| Model "forgets" earlier facts | Token count / window size | Summary memory, RAG, or structured DB facts |
| Wrong answers despite docs | Retrieval (`k`, chunk size, embedding model) | Re-chunk, hybrid search, cite sources in prompt |
| Cost spike | Messages array growth | Hard cap turns; summarize; cache embeddings |
| Duplicate / contradictory replies | Multiple memory sources unsynced | Single source of truth; version user profile row |
| PII in logs | What you persist | Redact before store; TTL on conversation tables |

## Pros/Cons or Trade-offs
- **Single-shot Q&A** with no follow-up — skip memory infrastructure entirely.
- **Strict audit trail required**
- **Real-time collaborative editing** — use CRDT/OT, not chat history as state.
