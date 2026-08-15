[[Security]] [[NAT Traversal]] [[ICE (Interactive Connectivity Establishment)]] [[STUN (Session Traversal Utilities for NAT)]] [[NAT (Network Address Translation)]] [[WebRTC]] [[Relay server]] [[WebRTC Signaling channels]]

# TURN server (Traversal Using Relays around NAT)

> TURN relays media through a server when two peers cannot punch through NATs — last resort path, not the first try.

## Interview Relevance

WebRTC interviews: TURN is the relay fallback when ICE cannot find a direct path — cost, auth, and bandwidth matter.

## Sources

- [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656) — deep-dive
- [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489) — overview

## Core Definition

TURN relays media through a server when peers cannot punch through NATs; ICE tries direct/STUN paths first and TURN last.

## Key Concepts

```txt
Peer A ──UDP/TCP──► TURN ◄──UDP/TCP── Peer B
                      │
                 media relayed
```

Unlike [[STUN (Session Traversal Utilities for NAT)]] (discover only), TURN **carries** the bytes. Used when firewalls or symmetric NAT block hole punching. ICE still **chooses** TURN only after cheaper paths fail (unless you force `relay`).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Relay candidate** | Address on the TURN box | “Relay means media goes via TURN.” |
| **Allocation** | Server reserves relay ports for a client | “Client asks TURN for an allocation.” |
| **Permission / channel** | Who may send to that allocation | “TURN only forwards allowed peers.” |
| **Bandwidth cost** | Server sees full media bitrate | “TURN is expensive — prefer direct.” |
| **Short-lived creds** | Time-limited username/password | “Never ship long-lived TURN secrets in the client.” |

### How the story goes

1. Client authenticates to TURN and gets an **allocation** (relay address).
2. That relay address becomes an ICE **relay** candidate.
3. If ICE nominates that pair, A↔B media flows A→TURN→B.

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

operations checklist: coturn (or cloud TURN), TLS on 443, REST API for time-limited credentials, monitor relay bandwidth.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| ICE fails, no relay candidates | TURN auth / DNS / firewall | Fix creds; open 3478/443; test `turnutils_uclient` |
| Works only with `relay` policy | Direct paths blocked | Keep TURN; optional dual-stack |
| Huge egress bill | Everyone on relay | Fix UDP/STUN path; audit ICE failures |
| 401 on allocate | Clock skew / bad HMAC | Sync NTP; verify REST secret |
| One-way audio on TURN | Permissions / channel bind | Check peer reflexive addresses allowed |

## Real-World Applications

Corporate firewalls that block UDP P2P force WebRTC calls through a TURN relay with time-limited credentials.

## Pros/Cons or Trade-offs

- **Pro:** Calls still connect when symmetric NATs/firewalls block direct paths.
- **Con:** Same LAN / open UDP — host or STUN paths are enough; skip TURN cost.
- **Con:** Server-centric apps — client↔your HTTPS API needs no TURN.

## Comparison

- vs [[STUN (Session Traversal Utilities for NAT)]]: relay vs address discovery.
- vs hosting media SFU: TURN is a packet relay for ICE; SFUs are application media servers.

## Mistakes to Avoid

- TURN is not signaling — signaling swaps SDP; TURN only relays media/data after ICE picks it.
- Long-lived passwords in JS — anyone can drain your bandwidth. Issue short-lived credentials from your API.
- Capacity — plan for worst-case simultaneous relay bitrate × users who need it.
