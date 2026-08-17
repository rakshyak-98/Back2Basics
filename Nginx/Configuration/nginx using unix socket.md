[[Configuration]] [[nginx stream]] [[Nginx internals]] [[Express middleware]]

# Nginx + Unix Domain Socket Upstream

> Same-host upstream over a unix socket — skip TCP loopback for lower latency and no port conflicts; socket permissions must allow Nginx to connect.

```txt
        Nginx + Unix Domai ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Platform reviews ask why unix sockets beat `127.0.0.1`, how to fix 502 per…

## Sources
- [nginx.org — proxy_pass (unix)](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass) — deep-dive
- [man unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html) — overview
- [systemd — RuntimeDirectory](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#RuntimeDirectory=) — overview

## Key Concepts
- **Why unix sockets:** Avoid TCP/IP stack on loopback
- **Permissions:** Socket file mode + directory ownership so the Nginx user (e.g
- **Stale sockets:** Crash leaves a socket file that blocks bind — remove in `ExecStartPre`.
- **WebSocket still works:** Set `Upgrade` / `Connection` headers as with TCP upstreams.


- **Core:** Nginx can reverse-proxy to an HTTP upstream bound on a unix domain socket (`h…

## Technical Details
- Unix sockets avoid TCP overhead on the same host (often ~20–30% throughput ga…
- Trade-off: socket file permissions and cleanup on restart.

### App side (Express)

```javascript
import express from 'express';
import fs from 'fs';

const app = express();
const SOCKET_PATH = '/var/run/my-api/app.sock';

if (fs.existsSync(SOCKET_PATH)) {
  fs.unlinkSync(SOCKET_PATH);   // stale socket blocks bind
}

app.listen(SOCKET_PATH, () => {
  fs.chmodSync(SOCKET_PATH, 0o660);
  console.log(`Listening on ${SOCKET_PATH}`);
});
```

```bash
sudo mkdir -p /var/run/my-api
sudo chown www-data:www-data /var/run/my-api
```

### systemd unit

```ini
[Unit]
Description=My Node.js API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/my-api
ExecStartPre=/bin/rm -f /var/run/my-api/app.sock
ExecStart=/usr/bin/node dist/server.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

### Nginx upstream

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    location / {
        proxy_pass http://unix:/var/run/my-api/app.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

- Syntax: `http://unix:/absolute/path.sock` — no host/port.

```bash
ls -la /var/run/my-api/app.sock
curl --unix-socket /var/run/my-api/app.sock http://localhost/health
sudo nginx -t && sudo systemctl reload nginx
```

| Method | Requests/sec (typical) | Latency |
|--------|------------------------|---------|
| TCP `127.0.0.1:3000` | ~18,500 | ~2.1 ms |
| Unix socket | ~24,000+ | ~1.4 ms |

- Numbers vary by hardware and payload

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | Socket missing or wrong path | `ls -la`; app running? |
| 502 Permission denied | Nginx user can't access socket | Shared group `www-data`; mode `660` |
| EADDRINUSE on socket | Stale socket after crash | `ExecStartPre=rm -f`; manual `rm` |
| curl unix works, Nginx 502 | Typo in `proxy_pass` path | Paths must match exactly |
| Intermittent 502 after restart | Nginx before app ready | systemd ordering + health check |

## Mistakes to Avoid
- **Mistake:** `chmod 777` on the socket — use group membership instead
- **Mistake:** Forgetting `/var/run` is tmpfs
- **Mistake:** Assuming WebSockets need TCP

## Pros/Cons or Trade-offs
- **Pro:** Latency and port hygiene on single-host deploys.
- **Con:** Local only — multi-host upstreams need TCP/HTTP.
- **Con:** Local development is often simpler on a TCP port; switch to socket for production.

## Comparison
- vs TCP `127.0.0.1:PORT`: sockets win on same host
- vs [[nginx stream]]: stream is L4 listen/proxy


### Use cases
- Node/Python/PHP-FPM on the same VM as Nginx, proxying over `/run/app/app.sock…
