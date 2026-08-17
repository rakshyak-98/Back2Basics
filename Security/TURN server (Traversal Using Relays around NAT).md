[[Security]] [[NAT Traversal]] [[ICE (Interactive Connectivity Establishment)]] [[STUN (Session Traversal Utilities for NAT)]] [[NAT (Network Address Translation)]] [[WebRTC]] [[Relay server]] [[WebRTC Signaling channels]]

# TURN server (Traversal Using Relays around NAT)

> TURN relays media through a server when two peers cannot punch through NATs — last resort path, not the first try.

```txt
        TURN server (Trave ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** WebRTC reviews: TURN is the relay fallback when ICE cannot find a direct p…

## Sources
- [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656) — deep-dive
- [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489) — overview

## Key Concepts
- **Core:** TURN relays media through a server when peers cannot punch through NATs

## Technical Details
```js
const pc = new RTCPeerConnection({
  iceServers: [{
    urls: [
      'turn:turn.example.com:3478?transport=udp',
      'turn:turn.example.com:3478?transport=tcp',
      'turns:turn.example.com:443?transport=tcp', // TLS — corporate-friendly
    ],
    username: shortLivedUser,
    credential: shortLivedPass,
  }],
  iceTransportPolicy: 'all', // 'relay' forces TURN for debug
})
```

- operations checklist: coturn (or cloud TURN), TLS on 443, REST API for time-l…

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| ICE fails, no relay candidates | TURN auth / DNS / firewall | Fix creds; open 3478/443; test `turnutils_uclient` |
| Works only with `relay` policy | Direct paths blocked | Keep TURN; optional dual-stack |
| Huge egress bill | Everyone on relay | Fix UDP/STUN path; audit ICE failures |
| 401 on allocate | Clock skew / bad HMAC | Sync NTP; verify REST secret |
| One-way audio on TURN | Permissions / channel bind | Check peer reflexive addresses allowed |

## Mistakes to Avoid
- **Mistake:** TURN is not signaling
- **Mistake:** Long-lived passwords in JS
- **Mistake:** Capacity

## Pros/Cons or Trade-offs
- **Pro:** Calls still connect when symmetric NATs/firewalls block direct paths.
- **Con:** Same LAN / open UDP — host or STUN paths are enough; skip TURN cost.
- **Con:** Server-centric apps — client↔your HTTPS API needs no TURN.

## Comparison
- vs [[STUN (Session Traversal Utilities for NAT)]]: relay vs address discovery.
- vs hosting media SFU: TURN is a packet relay for ICE; SFUs are application media servers.


### Use cases
- Corporate firewalls that block UDP P2P force WebRTC calls through a TURN rela…
