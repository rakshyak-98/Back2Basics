[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Strategy pattern]]

# Chain of Responsibility

> Chain of Responsibility passes a request along a chain of handlers until one handles it — decoupling sender from receiver and allowing dynamic handler ordering.

## Structure

```
Handler1 → Handler2 → Handler3 → (done or drop)
   handle(req) {
     if (canHandle) process
     else next.handle(req)
   }
```

Examples: logging filters (debug → info → error), middleware stacks, UI event bubbling, approval workflows.

## Middleware shape (HTTP)

```text
request → auth → rateLimit → validate → handler → response
```

Each link calls `next()` or short-circuits with a response.

## When to use

- Multiple objects *might* handle a request; exact handler unknown at compile time.
- Ordered processing with optional early exit.

## Pitfalls

- Request never handled — ensure terminal handler or explicit failure.
- Hidden order dependency — document chain sequence.
- Debugging long chains — trace which handler acted.

## Sources

- Gamma et al., *Design Patterns* (Chain of Responsibility)
- [Chain-of-responsibility pattern — Wikipedia](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)
