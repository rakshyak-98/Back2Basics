[[NAT (Network Address Translation)]] [[STUN (Session Traversal Utilities for NAT)]] [[TURN server (Traversal Using Relays around NAT)]] [[UDP]] [[webSocket]] [[ICE (Interactive Connectivity Establishment)]]

# NAT Traversal

> NAT traversal techniques let two peers behind address translators set up direct or relayed sessions — when it fails, one side is still symmetric NAT or UDP is blocked.

```txt
        NAT Traversal ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use NAT traversal to probe WebRTC/P2P depth: why inbound connect…

## Sources
- [RFC 8445 — Interactive Connectivity Establishment (ICE)](https://www.rfc-editor.org/rfc/rfc8445) — deep-dive
- [RFC 5389 — STUN](https://www.rfc-editor.org/rfc/rfc5389) — deep-dive
- [Wikipedia — NAT traversal](https://en.wikipedia.org/wiki/NAT_traversal) — overview

## Technical Details
- [[NAT (Network Address Translation)]] hides internal endpoints.
- Inbound connections need a pre-existing mapping or a relay.

- Interactive Connectivity Establishment (RFC 8445) gathers **candidate** addre…

```
Host candidate      192.168.1.5:9xxx     (local)
Server reflexive    203.0.113.2:5xxx     (via STUN)
Relayed             turn.example:3478    (via TURN)
```

- Pairs are checked with STUN binding requests; the best working path wins.

| Component | Role |
|-----------|------|
| [[STUN (Session Traversal Utilities for NAT)]] | Discover public IP:port; hole punching |
| [[TURN server (Traversal Using Relays around NAT)]] | Relay when direct UDP/TCP fails |
| ICE | Orchestrates checks and priority |

- NAT behavior types:

| Type | Traversal difficulty |
|------|---------------------|
| Full cone | Easier — same mapping for any remote |
| Restricted cone | Needs correct remote IP |
| Port restricted | Needs IP + port match |
| Symmetric | New mapping per destination — hard; often needs TURN |

- Non-WebRTC patterns:

- Outbound-only TCP (client connects first)
- [[UDP]] keepalives to refresh mappings
- Application-level tunnels over HTTPS ([[webSocket]], WebRTC data channel)

## Mistakes to Avoid
- **Mistake:** Shipping WebRTC with STUN only and no TURN
- **Mistake:** Treating "symmetric NAT" as rare
- **Mistake:** Forgetting [[UDP]] keepalives
- **Mistake:** Assuming TCP always solves traversal

## Pros/Cons or Trade-offs
- **Pro:** Direct peer paths cut latency and server bandwidth when hole punching succeeds.
- **Con:** Symmetric NAT, UDP blocks, and short idle timers force TURN; relays add cost and a dependency on infrastructure.

## Comparison
- vs plain [[NAT (Network Address Translation)]]: NAT is the translation middle…


### Use cases
- WebRTC calls, multiplayer games, and any peer-to-peer data channel across hom…
