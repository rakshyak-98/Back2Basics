<!-- note-strategy: operational -->
[[Protocol]] [[TURN server (Traversal Using Relays around NAT)]] [[STUN (Session Traversal Utilities for NAT)]] [[ICE (Interactive Connectivity Establishment)]] [[NAT Traversal]]

# Relay server

> Relay server — both peers dial out to a middle box that forwards bytes when they cannot connect directly through NAT.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Device A and Device B each open an *outbound* connection to the relay; the relay stitches those sockets and copies packets — inbound holes through NAT are not required.

```txt
Peer A ──outbound──► Relay ◄──outbound── Peer B
                       │
                  forwards A↔B
```

In WebRTC this is usually [[TURN server (Traversal Using Relays around NAT)]]. [[STUN (Session Traversal Utilities for NAT)]] only discovers addresses; the relay **carries** the media. [[ICE (Interactive Connectivity Establishment)]] picks relay only after cheaper paths fail.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Outbound-only** | Clients dial the relay | “NATs allow out; relay avoids inbound.” |
| **Allocation** | Relay reserves ports for a client | “TURN allocation is my relay address.” |
| **Hairpin / double NAT** | Complex home/CGNAT topologies | “Direct fails; relay still works.” |
| **TCP/TLS TURN** | Relay over allowed web ports | “When UDP dies, turns:443 saves the call.” |
| **Cost** | Server sees full bitrate | “Relays are the expensive fallback.” |

### When outbound is also blocked

Strict egress firewalls break STUN/TURN. Escapes (in order of commonality):

1. Allowlist TURN IPs/ports (best).
2. TURN over TLS/WebSocket on 443.
3. Corporate forward HTTP proxy (if supported).
4. VPN that exits where TURN is reachable.

---

## Standard config / commands

```js
// WebRTC: relay = TURN in iceServers
const pc = new RTCPeerConnection({
  iceServers: [{
    urls: [
      'turn:turn.example.com:3478?transport=udp',
      'turns:turn.example.com:443?transport=tcp',
    ],
    username: shortLivedUser,
    credential: shortLivedPass,
  }],
  iceTransportPolicy: 'all', // 'relay' = force relay for debug
})
```

```bash
# coturn smoke test
turnutils_uclient -v -u user -w pass turn.example.com
```

| Knob | Why it matters |
|------|----------------|
| Short-lived credentials | Long-lived secrets in clients get stolen |
| UDP + TCP/TLS listeners | Corporate nets block UDP |
| Bandwidth alerts | Silent “everyone on relay” burns money |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| ICE fails, no relay candidates | Auth / DNS / firewall to TURN | Fix creds; open 3478/443; test `turnutils_uclient` |
| Works only with `iceTransportPolicy: 'relay'` | Direct/STUN path broken | Keep relay; fix UDP/STUN for cost |
| Connect fails on corp Wi‑Fi | UDP egress filtered | Enable TURN TCP/TLS 443 |
| Huge egress bill | Most sessions nominated relay | Fix NAT/firewall; investigate ICE failure rate |
| One-way media via relay | Permissions / wrong peer addr | Check TURN permissions/channels |
| Outbound totally blocked | Proxy/VPN required | Allowlist or tunnel; otherwise no P2P |

---

## Gotchas

> [!WARNING]
> **Relay is not STUN** — if you only deploy STUN, hard NATs still fail.

> [!WARNING]
> **Forcing relay hides root cause** — fine for demos; in prod measure how often you need it.

> [!WARNING]
> **Reverse proxies ≠ TURN** — an HTTPS reverse proxy fronts your API; TURN is a media/data forwarder with allocations.

---

## When NOT to use

- **Same-LAN / host candidates already work** — don’t pay relay RTT and cost.
- **One-to-many broadcast** — CDN + [[HLS]]/[[DASH]], not per-viewer relays.
- **You control both ends with public IPs** — direct TCP/UDP or a normal media server is simpler.

---

## Related

[[TURN server (Traversal Using Relays around NAT)]] [[STUN (Session Traversal Utilities for NAT)]] [[ICE (Interactive Connectivity Establishment)]] [[NAT (Network Address Translation)]] [[NAT Traversal]] [[WebRTC]] [[P2P (Peer-to-Peer)]]
