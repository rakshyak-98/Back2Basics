[[Networking/UDP]] [[Security/TLS (Transport Layer Security)]] [[Security/https]] [[Networking/half-open connections]] [[Nginx/Configuration]]

# QUIC

> QUIC — (Quick UDP Internet Connections) moves transport into user space over UDP, integrating encryption and stream multiplexing. Designed to fix TCP head-of-line blocking and slow

```txt
        QUIC ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** QUIC/HTTP3 reviews test UDP transport literacy

## Sources
- [RFC 9000 — QUIC](https://www.rfc-editor.org/rfc/rfc9000) — deep-dive
- [Cloudflare — What is QUIC?](https://www.cloudflare.com/learning/performance/what-is-quic/) — overview

## Key Concepts
- **Note:** **QUIC** (Quick UDP Internet Connections) moves transport into user space ove…

```
HTTP/3
   │
   ▼
 QUIC (streams, crypto, congestion)
   │
   ▼
 UDP datagrams
   │
   ▼
 IP
```

| vs [[Networking/TCP]] + TLS + HTTP/2 | QUIC |
|--------------------------------------|------|
| 3-way TCP + TLS handshakes | Often 0-RTT / 1-RTT combined |
| One lost packet blocks all streams | Independent streams per connection |
| OS kernel TCP | Userspace implementations (Chrome, nginx quic) |

- **Note:** Originated by Jim Roskind at Google

## Technical Details
### Verify HTTP/3 on site

```bash
curl -I --http3 https://cloudflare.com
# or Chrome DevTools → Network → Protocol column → h3
```

### nginx HTTP/3 (example — requires quic module / recent nginx)

```nginx
server {
    listen 443 quic reuseport;
    listen 443 ssl;
    http2 on;
    http3 on;
    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    add_header Alt-Svc 'h3=":443"; ma=86400';
}
```

### Alt-Svc discovery

- Browsers upgrade from HTTP/2 via `Alt-Svc: h3=":443"`

### Firewall

```bash
# QUIC uses UDP 443 — TCP-only security groups block HTTP/3
sudo ufw allow 443/udp
```

### Debug packet loss impact

```bash
# Compare h2 vs h3 on lossy link — QUIC recovers per-stream
tc qdisc add dev eth0 root netem loss 1%
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Never see h3 | UDP 443 blocked | Open firewall; CDN QUIC toggle |
| Falls back to HTTP/2 | Alt-Svc missing/expired | Add `Alt-Svc` header; cert valid |
| 0-RTT replay concerns | Idempotent GET only | Disable 0-RTT for non-idempotent routes |
| CPU high on edge | QUIC in userspace | Hardware TLS; tune worker count |
| Connection migration fails | NAT rebinding | QUIC connection IDs — usually CDN handles |

## Mistakes to Avoid
- **Mistake:** Middleboxes that block UDP
- **Mistake:** **0-RTT data**
- **Mistake:** **Load balancer stickiness**
- **Mistake:** **Debugging**

## Pros/Cons or Trade-offs
- **Trade-off:** Internal east-west microservice mesh on trusted LAN — gRPC over HTTP/2 may be simpler operations.
- **Trade-off:** Legacy clients only — maintain dual stack until analytics show negligible h3 need.
