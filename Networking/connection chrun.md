[[half-open connections]] [[Epoll]] [[ss]] [[TCP]] [[webSocket]]

# connection churn (connection chrun)

> Churn is a high rate of short-lived TCP connections — each open/close costs handshake, ports, and CPU; idle timeout mismatch makes it worse.

## Interview Relevance

Interviewers use connection churn to test whether you can diagnose TIME_WAIT exhaustion, 502s after idle, and keepalive/timeout ladders across load balancer, app, and client pools — not just “scale more servers.”

## Sources

- [Linux TCP — tcp(7)](https://man7.org/linux/man-pages/man7/tcp.7.html) — deep-dive
- [AWS — Application Load Balancer idle timeout](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#connection-idle-timeout) — overview
- [ss(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ss.8.html) — overview

## Core Definition

Churn is a high rate of short-lived TCP connections (HTTP/1.0-style close per request, health checks, misconfigured pools) or idle timeout mismatch (load balancer closes while the client still thinks the connection is open).

## Key Concepts

| Pattern | Cost |
|---------|------|
| New TCP per HTTP request | SYN handshake + TLS (if HTTPS) every time |
| LB idle < app keepalive | Ghost requests, 502s, RST storms |
| No connection reuse | Ephemeral port / `TIME_WAIT` exhaustion |
| Aggressive health checks | Accept queue + churn even at zero user traffic |

## Technical Details

```
Client                    Load balancer              Server
  │── new TCP ───────────────────────────────────────►│  (expensive)
  │◄── response ─ close ────────────────────────────│
  │── new TCP ───────────────────────────────────────►│  repeat 1000/s
  │
  LB idle 60s closes ◄── client still sends ──► RST / half-open ([[half-open connections]])
```

**Align timeouts (LB < client < server or a consistent ladder):**

```
LB idle timeout:     60s   (AWS ALB default)
App keepalive:       65s+  (nginx keepalive_timeout 75s; Node server.keepAliveTimeout > LB)
Client pool TTL:     reuse sockets; idle < LB
```

```bash
# TIME_WAIT / state histogram
ss -s
ss -tan state time-wait | wc -l
ss -tan state close-wait | wc -l

# Who is churning (root for -p)
ss -tnp | awk '{print $6}' | sort | uniq -c | sort -rn | head

# Ephemeral port range
sysctl net.ipv4.ip_local_port_range
# default often 32768 60999 → ~28k outbound slots; TIME_WAIT holds each ~60s

# Kernel TIME_WAIT tuning (Linux) — know before tuning
sysctl net.ipv4.tcp_tw_reuse          # safe-ish for outbound client reuse (1)
sysctl net.ipv4.tcp_fin_timeout       # default 60 — how long FIN-WAIT-2 etc
# tcp_tw_recycle: REMOVED (broke NAT); never enable on guides

# nginx upstream keepalive (reduce churn to backend)
# upstream backend { server 127.0.0.1:8080; keepalive 32; }
# proxy_http_version 1.1; proxy_set_header Connection "";

# Node.js HTTP(S) server — MUST exceed LB idle timeout
# server.keepAliveTimeout = 65000;  // ms
# server.headersTimeout   = 66000;  // slightly higher (Node gotcha)
```

**HTTP keepalive headers:**

| Layer | Knob |
|-------|------|
| HTTP/1.1 | Default persistent unless `Connection: close` |
| Client (axios/fetch agent) | `keepAlive: true`, maxSockets pool |
| nginx → client | `keepalive_timeout 65;` |
| nginx → upstream | `keepalive` in upstream block |
| ALB/NLB | Idle timeout in console/Terraform |

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRNOTAVAIL` / can't connect out | `ss -tan state time-wait \| wc -l`; port range | Enable keepalive + reuse; fix pool; widen `ip_local_port_range` (band-aid) |
| 502 after idle period | LB access logs; `ss -ti` timers | Raise `keepAliveTimeout` above LB; enable HTTP keepalive |
| SYN flood appearance, low traffic | Health check interval; `ss -tan state syn-recv` | Reduce check frequency; use HTTP keepalive to backend |
| CPU on accept, low RPS | `ss -s`; strace accept loop | Connection per request — enable reuse / HTTP2 / multiplex |
| CLOSE-WAIT climbing | `ss -tan state close-wait -p` | App not closing sockets ([[Epoll]] event loop bug) |
| TLS handshake latency spikes | Metrics new conn rate | Session resumption; connection pooling; HTTP/2 |

**Node.js agent gotcha:** If `keepAliveTimeout` ≤ LB idle timeout, LB sends FIN first while Node still has a request in flight → **502** on next reuse. Set Node **65s+** when ALB is **60s**.

**Half-open after LB drop:** Client sends on a dead connection → RST or hang until timeout. Fix: keepalive probes + match timeouts; see [[half-open connections]].

```bash
# Quick churn rate estimate (two samples 5s apart)
ss -tan state established | wc -l; sleep 5; ss -tan state established | wc -l
# Plus timewait growth:
ss -tan state time-wait | wc -l
```

## Real-World Applications

HTTP APIs behind ALB/nginx, microservice meshes, and health-check-heavy platforms where connection reuse dominates latency and port usage.

**Example:** Node behind ALB returns intermittent 502 after quiet periods — `keepAliveTimeout` was 5s below ALB idle; raising it above the LB timeout stopped the RST-on-reuse failures.

## Pros/Cons or Trade-offs

- **Pro:** Aggressive short connections simplify some clients — no idle state to manage.
- **Con:** Handshake + TLS + TIME_WAIT cost scales with request rate, not payload size.
- **Con:** Widening ephemeral ports without fixing churn treats the symptom; TIME_WAIT still costs CPU and conntrack.
- **Trade-off:** HTTP/2 one TCP, many streams reduces handshake churn but still one connection to manage.

## Comparison

- vs long-lived [[webSocket]] / gRPC streams: different failure mode — read idle and proxy timeouts, not TIME_WAIT storms.
- vs UDP: no TIME_WAIT; different tools (`ss -u`).
- vs database pool churn: same CLOSE-WAIT / leak signatures in [[ss]], different pool knobs.

## Mistakes to Avoid

- Enabling `tcp_tw_recycle` from old blog posts — removed in Linux 4.12; breaks clients behind NAT.
- Widening `ip_local_port_range` as the primary fix instead of keepalive and pooling.
- Tuning `fin_timeout` to 5 globally — can break legitimate slow closes; fix application reuse first.
- Ignoring sidecar/service mesh hops — each hop needs keepalive alignment.
- Monitoring with `curl` every 10s from 50 pods without keepalive — artificial churn.
