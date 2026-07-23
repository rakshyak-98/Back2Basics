[[HTTP module]] [[TCP]] [[SOCKS (Socket Secure)]] [[Configuration]]

# WebSocket

> One-line: full-duplex framed messages over a single TCP connection, bootstrapped via HTTP Upgrade — **RFC 6455**.

## Mental model

WebSocket starts as HTTP/1.1 with an **Upgrade** handshake, then switches to a binary-framed protocol. No repeated HTTP headers per message — ideal for push, chat, live dashboards.

```
Client                          Server / Proxy
  │  GET /ws HTTP/1.1              │
  │  Upgrade: websocket            │
  │  Connection: Upgrade           │
  │  Sec-WebSocket-Key: ...        │
  ├───────────────────────────────►│
  │◄───────────────────────────────┤  101 Switching Protocols
  │  ◄──── framed messages ────►   │  (TCP stays open)
```

Browsers only speak `ws://` / `wss://`. They **cannot** use standard HTTP proxy env vars for WebSocket — needs HTTP CONNECT tunnel or [[SOCKS (Socket Secure)]].

## Standard config / commands

### Nginx reverse proxy (production baseline)

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream ws_backend {
    ip_hash;                    # sticky sessions — see Gotchas
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
}

location /ws/ {
    proxy_pass http://ws_backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_read_timeout 3600s;   # idle WS connection — default 60s kills long polls
    proxy_send_timeout 3600s;
    proxy_connect_timeout 10s;
}
```

### Client-side proxy (debug only)

```shell
# Force Chrome through SOCKS for WS debugging
chrome --proxy-server="socks5://127.0.0.1:1080"
```

### Quick connectivity test

```shell
# websocat / wscat
wscat -c wss://example.com/ws/
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  https://example.com/ws/
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works direct, fails via nginx | `curl -i` through proxy; nginx error log | Missing `Upgrade`/`Connection` headers; add `map` block above |
| 502 after ~60s idle | nginx `proxy_read_timeout` (default 60s) | Raise timeout; align with app heartbeat interval |
| 504 on connect | `proxy_connect_timeout`; upstream down | Fix backend listen; check upstream block |
| Random disconnects behind LB | LB idle timeout vs app ping interval | Send WS ping every `(idle_timeout / 2)`; enable TCP keepalive |
| Messages hit wrong backend pod | LB algorithm (round-robin) | Sticky sessions: `ip_hash`, cookie-based stickiness, or shared pub/sub backplane |
| `403` / `400 Bad Request` on upgrade | WAF blocking Upgrade header | Allowlist `/ws/` path; disable request body inspection on upgrade |
| SSL termination breaks WS | Client uses `wss://`, origin uses `ws://` internally | Terminate TLS at nginx; proxy to backend over HTTP with correct `X-Forwarded-Proto` |
| Reconnect storm after deploy | Connection count spike, CPU peg | Implement exponential backoff + jitter on client; drain old pods gracefully |

## Gotchas

> [!WARNING]
> **Default nginx 60s timeout** is the #1 production WebSocket killer. Always set `proxy_read_timeout` explicitly.

> [!WARNING]
> **Sticky sessions required** when state lives in memory on one pod. Round-robin without a shared backplane = messages arrive on pod A while session state is on pod B.

- **HTTP/2 and HTTP/3** do not carry WebSocket the same way — browsers still upgrade over HTTP/1.1 to the edge; ALB/ingress may need dedicated WS listener rules.
- **`Connection: Upgrade` is hop-by-hop** — every proxy in the path must forward it; CDN defaults often strip it.
- **Reconnect logic**: clients should resubscribe on `onopen`; server must tolerate duplicate session IDs; use versioned state or idempotent join.
- **Backpressure**: slow consumer can buffer unbounded in kernel; monitor send queue; drop or disconnect abusive clients.
- **Health checks**: HTTP GET on `/health` doesn't prove WS works — add lightweight WS ping probe or separate TCP check on WS port.

### Reconnect pattern (client sketch)

```javascript
function connect(url, attempt = 0) {
  const ws = new WebSocket(url);
  ws.onopen = () => { attempt = 0; resubscribeAll(); };
  ws.onclose = () => {
    const delay = Math.min(30000, 1000 * 2 ** attempt) + Math.random() * 500;
    setTimeout(() => connect(url, attempt + 1), delay);
  };
  return ws;
}
```

## When NOT to use

- High-frequency fan-out to millions of clients → dedicated pub/sub ([[MQTT]], SSE, or managed realtime service) scales better operationally.
- Request/response CRUD → ordinary HTTP/REST or [[gRPC]] is simpler to cache, debug, and load-balance.

## Related

[[HTTP module]] · [[TCP]] · [[SOCKS (Socket Secure)]] · [[Configuration]] · [[half-open connections]] · [[concurrent connection]]
