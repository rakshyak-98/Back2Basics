[[HTTP module]] [[TCP]] [[SOCKS (Socket Secure)]] [[Configuration]] [[half-open connections]] [[concurrent connection]]

# WebSocket

> Full-duplex framed messages over a single TCP connection, bootstrapped via HTTP Upgrade — **RFC 6455**.

```txt
        WebSocket ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask WebSocket to see if you know the Upgrade handshake, why prox…

## Sources
- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455.html) — deep-dive
- [MDN — Writing WebSocket servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers) — overview
- [Wikipedia — WebSocket](https://en.wikipedia.org/wiki/WebSocket) — overview

## Key Concepts
- **Upgrade handshake:** `Upgrade: websocket` + `Sec-WebSocket-Key` → `101 Switching Protocols` then f…
- **Full-duplex:** either side pushes anytime → chat, live dashboards, collaborative editors.
- **`ws://` / `wss://`:** browser schemes; TLS via `wss://` (often terminated at the edge).
- **Hop-by-hop `Connection: Upgrade`:** every proxy must forward it — CDNs often strip by default.
- **Sticky sessions / shared backplane:** in-memory session state needs affinity or pub/sub across pods.


- **Core:** WebSocket starts as HTTP/1.1 with an Upgrade handshake, then switches to a bi…

## Technical Details
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

- Browsers only speak `ws://` / `wss://`.
- They **cannot** use standard HTTP proxy environment variables for WebSocket

### Nginx reverse proxy (production baseline)

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream ws_backend {
    ip_hash;                    # sticky sessions — see Mistakes
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

- HTTP/2 and HTTP/3 do not carry WebSocket the same way

## Mistakes to Avoid
- **Mistake:** Leaving nginx’s default 60s `proxy_read_timeout`
- **Mistake:** Round-robin without sticky sessions or a shared backplane when s…
- **Mistake:** Assuming HTTP GET `/health` proves WS works
- **Mistake:** Missing reconnect/backoff
- **Mistake:** Ignoring backpressure

## Pros/Cons or Trade-offs
- **Pro:** Low overhead after handshake; true bidirectional push on one connection.
- **Con:** Stateful; harder to load-balance than plain HTTP without sticky sessions or a shared backplane.
- **Con:** Idle timeouts at every hop (proxy, LB, NAT) — heartbeats are mandatory in production.

## Comparison
- vs ordinary HTTP/REST or [[gRPC]]: request/response CRUD is simpler to cache, debug, and load-bal…
- vs SSE: SSE is server→client over HTTP; WebSocket is full-duplex.
- vs high-frequency fan-out to millions of clients: dedicated pub/sub ([[MQTT]], SSE, or managed re…


### Use cases
- Live dashboards, chat, collaborative editors, and game lobbies use WebSocket …

- **Example:** Connections die every ~60s behind nginx
