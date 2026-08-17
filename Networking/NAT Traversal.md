[[NAT (Network Address Translation)]] [[STUN (Session Traversal Utilities for NAT)]] [[TURN server (Traversal Using Relays around NAT)]] [[UDP]] [[webSocket]] [[ICE (Interactive Connectivity Establishment)]]

# NAT Traversal

> NAT traversal techniques let two peers behind address translators set up direct or relayed sessions — when it fails, one side is still symmetric NAT or UDP is blocked.





## Interview Relevance
Interviewers use NAT traversal to probe WebRTC/P2P depth: why inbound connections fail behind NAT, what STUN vs TURN do, ICE candidate types, and when symmetric NAT forces a relay.

## Sources
- [RFC 8445 — Interactive Connectivity Establishment (ICE)](https://www.rfc-editor.org/rfc/rfc8445) — deep-dive
- [RFC 5389 — STUN](https://www.rfc-editor.org/rfc/rfc5389) — deep-dive
- [Wikipedia — NAT traversal](https://en.wikipedia.org/wiki/NAT_traversal) — overview

## Recall Cues
- Why do interviewers care about Interviewers use NAT traversal to probe WebRTC/P2P depth: why inbound connections fail behind NAT, what STUN vs TURN do, ICE candidate types, and when symmetric NAT forces a relay?
- What mistake is **Shipping WebRTC with STUN only and no TURN — many real networks will never get a direct path**?
- What mistake is **Treating "symmetric NAT" as rare — enterprise and carrier-grade NAT often need relay**?
- What mistake is **Forgetting [[UDP]] keepalives — mappings expire and the "working" path dies mid-session**?
- What mistake is **Assuming TCP always solves traversal — many NATs still need outbound-first patterns or HTTPS tunnels**?

## Technical Details
[[NAT (Network Address Translation)]] hides internal endpoints. Inbound connections need a pre-existing mapping or a relay.

Interactive Connectivity Establishment (RFC 8445) gathers **candidate** addresses:

```
Host candidate      192.168.1.5:9xxx     (local)
Server reflexive    203.0.113.2:5xxx     (via STUN)
Relayed             turn.example:3478    (via TURN)
```

Pairs are checked with STUN binding requests; the best working path wins.

| Component | Role |
|-----------|------|
| [[STUN (Session Traversal Utilities for NAT)]] | Discover public IP:port; hole punching |
| [[TURN server (Traversal Using Relays around NAT)]] | Relay when direct UDP/TCP fails |
| ICE | Orchestrates checks and priority |

NAT behavior types:

| Type | Traversal difficulty |
|------|---------------------|
| Full cone | Easier — same mapping for any remote |
| Restricted cone | Needs correct remote IP |
| Port restricted | Needs IP + port match |
| Symmetric | New mapping per destination — hard; often needs TURN |

Non-WebRTC patterns:

- Outbound-only TCP (client connects first)
- [[UDP]] keepalives to refresh mappings
- Application-level tunnels over HTTPS ([[webSocket]], WebRTC data channel)

## Mistakes to Avoid
- Shipping WebRTC with STUN only and no TURN — many real networks will never get a direct path.
- Treating "symmetric NAT" as rare — enterprise and carrier-grade NAT often need relay.
- Forgetting [[UDP]] keepalives — mappings expire and the "working" path dies mid-session.
- Assuming TCP always solves traversal — many NATs still need outbound-first patterns or HTTPS tunnels.

## Comparison
vs plain [[NAT (Network Address Translation)]]: NAT is the translation middlebox; traversal is the set of techniques (STUN/TURN/ICE, keepalives, outbound-first TCP) that restore reachability despite it.

## Real-World Applications
WebRTC calls, multiplayer games, and any peer-to-peer data channel across home/office NATs. Example: a video call works on corporate Wi-Fi only after TURN is enabled — STUN candidates fail because the firewall blocks UDP or NAT is symmetric.

## Pros/Cons or Trade-offs
- **Pro:** Direct peer paths cut latency and server bandwidth when hole punching succeeds.
- **Con:** Symmetric NAT, UDP blocks, and short idle timers force TURN; relays add cost and a dependency on infrastructure.
