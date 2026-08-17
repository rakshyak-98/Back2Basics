[[Networking]] [[webSocket]] [[ICMP]] [[half-open connections]] [[TCP]] [[Network error]]

# auto-pong

> Auto-pong answers a ping automatically — prove the path is alive without app-level chatter.

```txt
        auto-pong ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use ping/pong to separate **protocol keepalives** (WebSocket con…

## Sources
- [RFC 6455 — The WebSocket Protocol (Ping/Pong)](https://www.rfc-editor.org/rfc/rfc6455#section-5.5.2) — deep-dive
- [RFC 792 — Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792) — deep-dive
- [MDN — WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) — overview

## Key Concepts
- **Ping / pong:** probe + mandatory reply → control frames, not business payload.
- **Auto-pong:** reply without app code → kernel/WS stack answers so timers don’t expire.
- **Keepalive:** periodic probes on idle links → detect half-open [[TCP]] / dead NAT mappings.
- **RTT:** time ping→pong → latency sample for the control path.
- **ICMP echo:** classic `ping` tool → network reachability, not HTTP health.


- **Core:** Auto-pong is a stack-level reply to a ping probe (WebSocket pong frames, kern…

## Technical Details
```txt
WebSocket:  ping frame  →  auto pong frame
ICMP:       Echo Request →  Echo Reply
App:        {type:"ping"} → {type:"pong"}  (if you build it)
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| WS closes idle | No ping/pong; proxy timeout | Enable protocol ping ≤ proxy idle |
| Ping never answered | Auto-pong disabled / filtered | Fix library flags; allow ICMP |
| False “dead” peers | Interval too aggressive | Back off; require N misses |
| High CPU on huge fan-out | Ping storm | Jitter intervals; sample subset |
| ICMP works, app dead | Only L3 alive | Add app health on the real port |

## Mistakes to Avoid
- **Mistake:** Treating ICMP success as proof the app is up
- **Mistake:** Assuming all proxies forward WebSocket control frames
- **Mistake:** App-level JSON ping without a pong handler
- **Mistake:** Using ping flood as a load test or as the only authentication he…

## Pros/Cons or Trade-offs
- **Pro:** Cheap liveness without inventing JSON heartbeat schemas.
- **Con:** ICMP success ≠ service up — port 443 can still be down.
- **Con:** Aggressive intervals on huge fan-out waste CPU and battery.

## Comparison
- vs app-level JSON ping: protocol frames are answered by the stack
- vs [[TCP]] keepalive: different layer; pick one thoughtfully — don’t triple-probe blindly.
- vs HTTP health checks: hit the real application port/path; don’t rely on ICMP alone.


### Use cases
- Chat backends, IoT device tunnels, and game servers keep WebSocket or TCP ses…

- **Example:** Connections drop after 60s of silence behind a load balancer
