[[Python]] [[uwsgi]] [[wheel]] [[GIL (Global interpreter lock)]]

# ASGI

> Asynchronous Server Gateway Interface — standard way async Python web servers talk to apps (HTTP, WebSocket, lifespan).

```txt
        ASGI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Backend reviews contrast WSGI vs ASGI: sync workers vs async event loop, W…

## Sources
- [ASGI specification](https://asgi.readthedocs.io/en/stable/specs/main.html) — deep-dive
- [ASGI introduction](https://asgi.readthedocs.io/en/stable/introduction.html) — overview
- [Wikipedia — ASGI](https://en.wikipedia.org/wiki/Asynchronous_Server_Gateway_Interface) — overview

## Key Concepts
- **Scope / receive / send:** connection metadata dict + awaitable channels for events → supports multi-eve…
- **Protocol types:** HTTP, WebSocket, lifespan (`scope["type"]`) → one process can speak several p…
- **WSGI compatibility:** run sync apps in a thread pool so they don’t block the event loop
- **Servers vs apps:** Uvicorn/Hypercorn are servers; FastAPI/Starlette/Django ASGI are applications


- **Core:** ASGI defines a single async callable `application(scope, receive, send)`. Ser…

## Technical Details
```python
async def application(scope, receive, send):
    if scope["type"] != "http":
        return
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [[b"content-type", b"text/plain"]],
    })
    await send({"type": "http.response.body", "body": b"hello"})
```

```bash
uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000
```

- Typical stack: Nginx/Caddy → ASGI server → framework.
- Contrast with [[uwsgi|uWSGI]] speaking WSGI to sync Django/Flask.

| Concern | WSGI | ASGI |
|---------|------|------|
| Concurrency model | Process/thread per request style | Event loop + async def |
| WebSockets | Not in the standard | First-class |
| Long-lived connections | Awkward | Natural |

## Mistakes to Avoid
- **Mistake:** Calling blocking libraries directly in async views
- **Mistake:** Assuming ASGI removes the need for multiple workers
- **Mistake:** Confusing “async framework” with “automatically fast”

## Pros/Cons or Trade-offs
- **Pro:** One interface for HTTP + WebSocket + startup/shutdown lifespan hooks.
- **Con:** Sync ORM calls inside `async def` block the loop — use async drivers or `to_thread` carefully; [[GIL (Global interpreter lock)|GIL]] still limits CPU-bound threads.

## Comparison
- vs WSGI (PEP 3333): request/response callable only; no native WebSocket.
- vs [[uwsgi|uWSGI]]: uWSGI is a server/process manager often used with WSGI


### Use cases
- Chat or notification service: FastAPI WebSocket endpoints on Uvicorn behind N…
