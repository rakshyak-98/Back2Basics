[[Python]] [[uwsgi]] [[wheel]] [[GIL (Global interpreter lock)]]

# ASGI

> Asynchronous Server Gateway Interface — standard way async Python web servers talk to apps (HTTP, WebSocket, lifespan).





## Interview Relevance
Backend interviews contrast WSGI vs ASGI: sync workers vs async event loop, WebSockets, and why FastAPI/Starlette/Django ASGI exist. Expect “when would you still use WSGI?”

## Sources
- [ASGI specification](https://asgi.readthedocs.io/en/stable/specs/main.html) — deep-dive
- [ASGI introduction](https://asgi.readthedocs.io/en/stable/introduction.html) — overview
- [Wikipedia — ASGI](https://en.wikipedia.org/wiki/Asynchronous_Server_Gateway_Interface) — overview

## Core Definition
ASGI defines a single async callable `application(scope, receive, send)`. Servers (Uvicorn, Hypercorn, Daphne) drive connections; frameworks implement the callable. It is the spiritual successor to WSGI and can wrap sync WSGI apps via `asgiref`.

## Key Concepts
- **Scope / receive / send:** connection metadata dict + awaitable channels for events → supports multi-event protocols, not just one request/response.
- **Protocol types:** HTTP, WebSocket, lifespan (`scope["type"]`) → one process can speak several protocols.
- **WSGI compatibility:** run sync apps in a thread pool so they don’t block the event loop — bridge, not magic parallelism.
- **Servers vs apps:** Uvicorn/Hypercorn are servers; FastAPI/Starlette/Django ASGI are applications — swap servers without rewriting business code.

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

Typical stack: Nginx/Caddy → ASGI server → framework. Contrast with [[uwsgi|uWSGI]] speaking WSGI to sync Django/Flask.

| Concern | WSGI | ASGI |
|---------|------|------|
| Concurrency model | Process/thread per request style | Event loop + async def |
| WebSockets | Not in the standard | First-class |
| Long-lived connections | Awkward | Natural |

## Real-World Applications
Chat or notification service: FastAPI WebSocket endpoints on Uvicorn behind Nginx, same codebase as REST — no separate socket.io process required for basic cases.

## Pros/Cons or Trade-offs
- **Pro:** One interface for HTTP + WebSocket + startup/shutdown lifespan hooks.
- **Con:** Sync ORM calls inside `async def` block the loop — use async drivers or `to_thread` carefully; [[GIL (Global interpreter lock)|GIL]] still limits CPU-bound threads.

## Comparison
- vs WSGI (PEP 3333): request/response callable only; no native WebSocket.
- vs [[uwsgi|uWSGI]]: uWSGI is a server/process manager often used with WSGI; ASGI is the interface (Uvicorn implements it).

## Mistakes to Avoid
- Calling blocking libraries directly in async views — stalls every connection on that worker.
- Assuming ASGI removes the need for multiple workers — still scale processes for CPU and blast radius.
- Confusing “async framework” with “automatically fast” — measure under load.
