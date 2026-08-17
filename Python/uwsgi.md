[[Python]] [[ASGI]] [[nginx config structure]] [[Nginx/Configuration/nginx using unix socket]]

# uwsgi

> uWSGI — application server/process manager that typically speaks WSGI to Python apps and proxies behind Nginx or another edge server.

```txt
        uwsgi ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Ops/backend interviews still see uWSGI with classic Django/Flask: master-work…

## Sources
- [uWSGI documentation](https://uwsgi-docs.readthedocs.io/en/latest/) — deep-dive
- [Wikipedia — uWSGI](https://en.wikipedia.org/wiki/Uwsgi) — overview

## Key Concepts
- **Master / workers:** master supervises workers that load the app
- **Configuration file:** commonly `uwsgi.ini` with `module`/`mount`, processes/threads, socket path, a…
- **Protocol:** native uwsgi protocol to Nginx is common; HTTP mode also exists
- **Not ASGI-first:** modern async/WebSocket stacks usually pick Uvicorn/Hypercorn


- **Core:** uWSGI runs your Python application in worker processes, accepts requests (Uni…

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

- Typical path: client → Nginx → `uwsgi_pass` to socket → workers → Django/Flas…

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 from Nginx | Socket perms / workers alive | Match user groups; restart; check logs |
| Stale code after deploy | Workers not reloaded | Graceful reload (`touch-reload` / signals) |
| Worker wedged | Slow view / deadlock | `harakiri`; profile the app |
| Memory growth | Leaks / too many workers | Cap processes; recycle with `max-requests` |

## Mistakes to Avoid
- **Mistake:** Running uWSGI as root with a world-writable socket
- **Mistake:** Equating “uWSGI” with “WSGI”
- **Mistake:** Ignoring graceful reload

## Pros/Cons or Trade-offs
- **Pro:** Battle-tested process management and rich knobs for WSGI apps.
- **Con:** Complex surface area; ASGI/WebSocket greenfield apps usually choose simpler ASGI servers.

## Comparison
- vs Gunicorn: both serve WSGI
- vs [[ASGI]]/Uvicorn: different interface — pick ASGI for async/WebSocket-native stacks.


### Use cases
- Long-lived Django monolith on VMs: Nginx terminates TLS, uWSGI holds 8 worker…
