[[Nginx]] [[Configuration]] [[ExpressJS]]

# Nginx + Unix Domain Socket Upstream

> One-line: skip TCP loopback — bind the app to a unix socket for lower latency and no port conflicts; permissions must allow Nginx to connect.

## Mental model

```
Client → Nginx :443 → unix:/var/run/my-api/app.sock → Node/Express
```

Unix sockets avoid TCP overhead on same host (~20–30% throughput gain in typical benchmarks). Tradeoff: socket file permissions and cleanup on restart.

---

## Standard config / commands

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

Create socket directory with correct owner:

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now my-api
pm2 start dist/server.js --name my-api --user www-data   # alternative
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

Syntax: `http://unix:/absolute/path.sock` — no host/port.

### Verify

```bash
ls -la /var/run/my-api/app.sock
curl --unix-socket /var/run/my-api/app.sock http://localhost/health
sudo nginx -t && sudo systemctl reload nginx
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | Socket missing or wrong path | `ls -la` socket; app running? |
| 502 Permission denied | Nginx user can't access socket | Shared group: `chgrp www-data` on dir + socket `660`; or run app as `www-data` |
| App won't start: EADDRINUSE on socket | Stale socket file after crash | `ExecStartPre=/bin/rm -f ...`; manual `rm` |
| Works via curl --unix-socket, 502 via Nginx | Typo in `proxy_pass` path | Paths must match exactly; no trailing slash issues like HTTP upstream |
| Intermittent 502 after restart | Race: Nginx reload before app ready | systemd `After=` + health check; `Restart=always` |

---

## Gotchas

> [!WARNING]
> **`/var/run` is tmpfs** — socket gone on reboot. systemd `RuntimeDirectory=my-api` creates `/run/my-api` automatically.

> [!WARNING]
> **`chmod 777` is a lazy fix** — use group membership (`www-data`) instead.

> [!WARNING]
> **WebSocket + unix socket works** — still set `Upgrade` / `Connection` headers.

| Method | Requests/sec (typical) | Latency |
|--------|------------------------|---------|
| TCP `127.0.0.1:3000` | ~18,500 | ~2.1 ms |
| Unix socket | ~24,000+ | ~1.4 ms |

Numbers vary by hardware and payload — directionally correct for same-host proxy.

---

## When NOT to use

- **Multi-host upstreams** — unix sockets are local only; use TCP or HTTP upstream.
- **Quick local dev** — TCP port is simpler; switch to socket in production.

---

## Related

[[Configuration]] [[nginx stream]] [[Express middleware]]
