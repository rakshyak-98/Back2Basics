[[TCP]] [[ss]] [[POSIX Socket]] [[Epoll]]

# Half-open connections

> One-line: TCP where one side has closed its write path (FIN sent) but the read path is still open — **Stevens, TCP/IP Illustrated**.

## Mental model

TCP is full-duplex: each direction has its own FIN/ACK lifecycle. **Half-open** means one peer has shut down its outbound byte stream while the other can still send.

```
  A (closed write)          B (still writing)
  ─────────────────────────────────────────
  A: FIN ─────────────────► B  (A done sending)
  A: ◄────────────────────── B  (B may still send data)
  A receives EOF when B FINs or RSTs
```

Common production triggers:
- Server calls `shutdown(SHUT_WR)` or `close()` after response; client still reading.
- Load balancer health-check closes idle side; app socket stuck in `CLOSE_WAIT` or `FIN_WAIT_2`.
- Client crashes without FIN → peer sees half-open until TCP keepalive or timeout fires.

> [!NOTE]
> Node.js does **not** support half-open by default. Sockets auto-close when either side sends or receives EOF unless `{ allowHalfOpen: true }`.

```javascript
const server = net.createServer({ allowHalfOpen: true });
// server.end() no longer tears down the socket — use socket.destroy() explicitly
```

## Standard config / commands

Inspect socket state — start with [[ss]]:

```shell
# Half-open / stuck teardown states
ss -tan state fin-wait-2
ss -tan state close-wait
ss -tan state last-ack

# Count by state (quick leak check)
ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn

# Who owns CLOSE_WAIT (usually the side that didn't close())
ss -tanp state close-wait

# Kernel TCP keepalive defaults (affects zombie half-opens)
sysctl net.ipv4.tcp_keepalive_time net.ipv4.tcp_keepalive_intvl net.ipv4.tcp_keepalive_probes
```

Enable keepalive on long-lived server sockets (detect dead peers without app heartbeat):

```c
int yes = 1;
setsockopt(fd, SOL_SOCKET, SO_KEEPALIVE, &yes, sizeof(yes));
// Linux: tune via TCP_KEEPIDLE, TCP_KEEPINTVL, TCP_KEEPCNT
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `CLOSE_WAIT` count climbing on app host | `ss -tanp state close-wait` → owning PID | App not calling `close()` on accepted sockets after client disconnect; fix lifecycle / use `finally` blocks |
| `FIN_WAIT_2` pile-up on server | `ss -tan state fin-wait-2` | Peer never ACK'd or never sent FIN; lower `tcp_fin_timeout` or enable `tcp_tw_reuse` where appropriate; fix client hang |
| Connection "hangs" after server `end()` | tcpdump: `FIN` from server, no `FIN` from client | Client half-open; set `{ allowHalfOpen: false }` or explicitly `destroy()` both sides |
| LB shows healthy, app thread pool exhausted | Compare LB idle timeout vs app socket timeout | Align timeouts; LB often 60s, app 300s → orphaned server-side sockets |
| One direction works, other EOF unexpectedly | `tcpdump -i any host <peer> and tcp[tcpflags] & (fin\|rst) != 0` | Trace who sent FIN/RST first; check middleware (nginx `proxy_read_timeout`) |
| Mass half-opens after deploy | Spike in `SYN-RECV` or `ESTAB` without traffic | Rolling deploy + draining; old pods still hold connections; use graceful shutdown + `SO_LINGER` review |

## Gotchas

> [!WARNING]
> **CLOSE_WAIT leak = application bug**, not kernel bug. The remote side already closed; your process must `close()` the fd. Restarting the process "fixes" it temporarily — the leak returns.

> [!WARNING]
> **`server.end()` vs `socket.destroy()`** in Node with `allowHalfOpen: true`: `end()` only half-closes; clients that never read will hold the fd until keepalive timeout.

- **Half-close vs half-open**: "Half-close" is the *action* (`shutdown(SHUT_WR)`); "half-open" is the *resulting state*.
- **RST vs FIN**: RST immediately aborts both directions; FIN allows graceful drain. Mixed behavior confuses apps expecting clean EOF.
- **Epoll edge-triggered**: If you don't read until EOF after peer FIN, you may miss the event and leak the fd.
- **NAT middleboxes**: Can drop idle half-open flows silently; app-level heartbeat beats relying on TCP keepalive alone (default 2h on Linux).

## When NOT to use

- Don't enable `allowHalfOpen: true` unless the protocol explicitly needs unidirectional shutdown (streaming upload/download with independent lifetimes).
- Don't tune `tcp_fin_timeout` / `tcp_tw_reuse` without measuring — aggressive values can break legitimate long-tail responses.

## Related

[[TCP]] · [[ss]] · [[Epoll]] · [[connection chrun]] · [[webSocket]]
