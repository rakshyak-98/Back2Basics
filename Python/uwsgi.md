[[Python]] [[ASGI]] [[nginx config structure]] [[Nginx/Configuration/nginx using unix socket]]

# uwsgi

> uWSGI — application server/process manager that typically speaks WSGI to Python apps and proxies behind Nginx or another edge server.





## Interview Relevance
Ops/backend interviews still see uWSGI with classic Django/Flask: master-worker model, Emperor mode, sockets vs HTTP, and when to prefer Gunicorn or an [[ASGI]] server instead.

## Sources
- [uWSGI documentation](https://uwsgi-docs.readthedocs.io/en/latest/) — deep-dive
- [Wikipedia — uWSGI](https://en.wikipedia.org/wiki/Uwsgi) — overview

## Core Definition
uWSGI runs your Python application in worker processes, accepts requests (Unix socket, TCP, or HTTP), and optionally manages lifecycle (reload, cheaper mode, harakiri timeouts). Despite the name, it is a server — WSGI is the Python calling convention it often uses.

## Key Concepts
- **Master / workers:** master supervises workers that load the app — crash isolation and graceful reload patterns.
- **Configuration file:** commonly `uwsgi.ini` with `module`/`mount`, processes/threads, socket path, and limits.
- **Protocol:** native uwsgi protocol to Nginx is common; HTTP mode also exists — match what the reverse proxy expects.
- **Not ASGI-first:** modern async/WebSocket stacks usually pick Uvicorn/Hypercorn; uWSGI remains strong in WSGI estates.

## Technical Details
```ini
[uwsgi]
chdir = /srv/myapp
module = myapp.wsgi:application
master = true
processes = 4
socket = /run/uwsgi/myapp.sock
chmod-socket = 660
vacuum = true
die-on-term = true
harakiri = 30
```

```bash
uwsgi --ini uwsgi.ini
uwsgi --http :8000 --module myapp.wsgi:application --processes 4
```

Typical path: client → Nginx → `uwsgi_pass` to socket → workers → Django/Flask.

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 from Nginx | Socket perms / workers alive | Match user groups; restart; check logs |
| Stale code after deploy | Workers not reloaded | Graceful reload (`touch-reload` / signals) |
| Worker wedged | Slow view / deadlock | `harakiri`; profile the app |
| Memory growth | Leaks / too many workers | Cap processes; recycle with `max-requests` |

## Real-World Applications
Long-lived Django monolith on VMs: Nginx terminates TLS, uWSGI holds 8 workers on a Unix socket, deploy touches a reload file for zero-downtime worker recycle.

## Pros/Cons or Trade-offs
- **Pro:** Battle-tested process management and rich knobs for WSGI apps.
- **Con:** Complex surface area; ASGI/WebSocket greenfield apps usually choose simpler ASGI servers.

## Comparison
- vs Gunicorn: both serve WSGI; Gunicorn is often simpler to reason about; uWSGI has more features (and footguns).
- vs [[ASGI]]/Uvicorn: different interface — pick ASGI for async/WebSocket-native stacks.

## Mistakes to Avoid
- Running uWSGI as root with a world-writable socket.
- Equating “uWSGI” with “WSGI” — one is software, one is a PEP interface.
- Ignoring graceful reload — dropping the socket on hard restart causes blips behind Nginx.
