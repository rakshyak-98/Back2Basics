[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Strategy pattern]]

# Chain of Responsibility

> Chain of Responsibility passes a request along a chain of handlers until one handles it — decoupling sender from receiver and allowing dynamic handler ordering.

```txt
        Chain of Responsib ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Chain of Responsibility probes handler pipelines

## Sources
- Gamma et al., *Design Patterns* (Chain of Responsibility) — deep-dive

## Key Concepts
```
Handler1 → Handler2 → Handler3 → (done or drop)
   handle(req) {
     if (canHandle) process
     else next.handle(req)
   }
```

- **Note:** Examples: logging filters (debug → info → error), middleware stacks, UI event…

## Technical Details
- **Middleware shape (HTTP):** 

```text
request → auth → rateLimit → validate → handler → response
```

- Each link calls `next()` or short-circuits with a response.

## Mistakes to Avoid
- **Mistake:** Request never handled
- **Mistake:** Hidden order dependency — document chain sequence
- **Mistake:** Debugging long chains — trace which handler acted

## Real-World Applications
- **Multiple objects:** Multiple objects *might* handle a request
- **Ordered processing:** Ordered processing with optional early exit.
