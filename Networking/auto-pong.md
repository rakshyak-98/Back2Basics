[[Networking]] [[webSocket]] [[ICMP]] [[half-open connections]]

# auto-pong

> Auto-pong answers a ping automatically — prove the path is alive without app-level chatter.

---

## Mental model

**Say it in one breath:** Peer sends ping; stack or library replies pong. Used for keepalive, RTT, and dead-connection detection.

```txt
WebSocket:  ping frame  →  auto pong frame
ICMP:       Echo Request →  Echo Reply
App:        {type:"ping"} → {type:"pong"}  (if you build it)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Ping / pong** | Probe + mandatory reply | “Control frames, not business payload.” |
| **Auto-pong** | Reply without app code | “Kernel/WS stack answers so timers don’t expire.” |
| **Keepalive** | Periodic probes on idle links | “Detect half-open TCP / dead NAT mappings.” |
| **RTT** | Time ping→pong | “Latency sample for the control path.” |
| **ICMP echo** | Classic `ping` tool | “Network reachability, not HTTP health.” |

---

## Standard config / commands

```js
// ws library — server auto-responds to ping frames by default
import WebSocket, { WebSocketServer } from 'ws'
const wss = new WebSocketServer({ port: 8080 })
wss.on('connection', (socket) => {
  socket.on('pong', () => { /* RTT / liveness */ })
  const t = setInterval(() => {
    if (socket.readyState === WebSocket.OPEN) socket.ping()
  }, 30000)
  socket.on('close', () => clearInterval(t))
})
```

```bash
# ICMP auto-reply (kernel, if not firewalled)
ping -c 3 192.168.1.1
```

| Knob | Why it matters |
|------|----------------|
| Ping interval | Faster detection vs battery/CPU |
| Idle timeout | LB/NAT may kill silent TCP |
| App vs protocol ping | Prefer WS/ICMP control; don’t overload JSON |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| WS closes idle | No ping/pong; proxy timeout | Enable protocol ping ≤ proxy idle |
| Ping never answered | Auto-pong disabled / filtered | Fix library flags; allow ICMP |
| False “dead” peers | Interval too aggressive | Back off; require N misses |
| High CPU on huge fan-out | Ping storm | Jitter intervals; sample subset |
| ICMP works, app dead | Only L3 alive | Add app health on the real port |

---

## Gotchas

> [!WARNING]
> **ICMP success ≠ service up** — port 443 can still be down.

> [!WARNING]
> **Some proxies strip WS control frames** — test through the real LB path.

> [!WARNING]
> **App-level JSON ping without pong handler** — one side “auto”, the other silent ⇒ flapping.

---

## When NOT to use

- **As the only authentication heartbeat** — authenticate sessions separately.
- **Flood ping for load tests** — use proper traffic generators.
- **Replacing TCP keepalive thoughtfully** — pick one layer; don’t triple-probe blindly.

---

## Related

[[Networking]] [[webSocket]] [[ICMP]] [[half-open connections]] [[TCP]] [[Network error]]
