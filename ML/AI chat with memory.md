[[GPT]] [[prompt]] [[prompt engineering]] [[scikitlearn]]

# AI chat with memory

> The model remembers nothing between API calls. You must send history, summaries, or retrieved docs each time.

---

## Mental model

Each request is independent. You build the prompt like this:

```txt
system prompt + retrieved docs + chat history + latest user message → model → reply
```

The model has a **token limit**. Long chats cost more, run slower, and drop early messages.

| Approach | What you keep | Tradeoff |
|----------|---------------|----------|
| **Full transcript** | Every message | Simple; hits limit fast |
| **Rolling window** | Last N turns | Cheap; forgets old facts |
| **Summary** | LLM-compressed history | Keeps themes; loses exact wording |
| **Vector RAG** | Search over docs and past turns | Scales well; bad search = bad answers |
| **Structured DB** | User prefs and facts in rows | Reliable; needs schema and extraction |

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

Annotate **why**: system prompt sets behavior; RAG adds facts; trimming saves cost and time.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Model "forgets" earlier facts | Token count / window size | Summarize, use RAG, or store facts in a DB |
| Wrong answers despite docs | Search quality (k, chunk size, embeddings) | Fix chunks and search; cite sources in prompt |
| Cost spike | Growing messages array | Cap turns; summarize; cache embeddings |
| Contradictory replies | Multiple memory sources out of sync | One source of truth; version user profile |
| PII in logs | What you store | Redact before save; set TTL on chat tables |

---

## Gotchas

> [!WARNING]
> **Client-side chat history** — users can edit it. Treat it as UI only. Store real memory on the server with user/session ID.

> [!WARNING]
> **Untrusted RAG text** — documents can contain prompt injection. Sanitize and tell the model to ignore instructions inside docs.

---

## When NOT to use

- **One-off questions** — no memory needed.
- **Strict audit trail** — use DB fields, not LLM summaries you cannot replay.
- **Live collaborative editing** — use CRDT/OT, not chat history as state.

---

## Related

[[GPT]] · [[prompt engineering]] · [[ANN]] · [[data preprocessing]]
