[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Strategy pattern]]

# Chain of Responsibility

> Chain of Responsibility passes a request along a chain of handlers until one handles it — decoupling sender from receiver and allowing dynamic handler ordering.

## Interview Relevance

Chain of Responsibility probes handler pipelines — ordering, short-circuiting, and who owns unhandled requests.

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

Examples: logging filters (debug → info → error), middleware stacks, UI event bubbling, approval workflows.

## Technical Details

**Middleware shape (HTTP)**

```text
request → auth → rateLimit → validate → handler → response
```

Each link calls `next()` or short-circuits with a response.

## Real-World Applications

- Multiple objects *might* handle a request; exact handler unknown at compile time.
- Ordered processing with optional early exit.

## Mistakes to Avoid

- Request never handled — ensure terminal handler or explicit failure.
- Hidden order dependency — document chain sequence.
- Debugging long chains — trace which handler acted.
