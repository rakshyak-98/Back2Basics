[[TCP]] [[webSocket]] [[WebRTC]] [[SOCKS (Socket Secure)]]

# IRC

> IRC (Internet Relay Chat) — clients join a server or network of servers for channels and DMs; text chat over a simple TCP protocol.

```txt
        IRC ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use IRC to probe simple line protocols, TLS versus cleartext por…

## Sources
- [RFC 1459 — Internet Relay Chat Protocol](https://datatracker.ietf.org/doc/html/rfc1459) — deep-dive
- [IRCv3 working group](https://ircv3.net/) — overview
- [Wikipedia — IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) — overview

## Technical Details
```txt
Client ──TCP 6667/6697──► IRC server ◄──► other servers (same network)
                              │
                         #channel / PRIVMSG
```

1. Client opens TCP (often TLS on 6697).
2. Registers nick; optional SASL/NickServ authentication.
3. `JOIN #channel` → receives traffic for that room.
4. Ops moderate with modes (`+o`, bans); services handle accounts.

```bash
# Quick smoke test (plain; prefer TLS in real use)
nc irc.libera.chat 6667
# NICK mybot
# USER mybot 0 * :mybot
# JOIN #example
# PRIVMSG #example :hello
# QUIT
```

```ini
# Typical client settings
Server = irc.example.net
Port   = 6697
SSL    = true
Nick   = alice
SASL   = true
```

| Knob | Why it matters |
|------|----------------|
| 6667 vs 6697 | Plain vs TLS — corporate and public nets expect TLS |
| SASL | Auth before join — required on many networks |
| Flood limits | Bots without rate limits get KLINE’d |

| Symptom | Check | Fix |
|---------|-------|-----|
| Connect timeout | DNS / firewall / wrong port | Try 6697 TLS; whitelist IRC ports |
| Nick in use | Collision / ghost session | Ghost via NickServ; pick unique nick |
| Can’t join channel | Ban / +i / +k key | Ask ops; check `MODE #chan` |
| Silent after connect | Need CAP/SASL or registration | Enable SASL; identify before JOIN |
| Bot banned for flood | Burst PRIVMSG | Pace messages; use server-side limits |
| Split / missing users | Net split between servers | Wait for sync; check network status |

## Mistakes to Avoid
- **Mistake:** Treating port 6667 as production
- **Mistake:** Confusing services (NickServ/ChanServ) with the IRC daemon
- **Mistake:** Bursting PRIVMSG from bots without rate limits

## Pros/Cons or Trade-offs
- **Pro:** Simple, scriptable, federated networks — low protocol overhead.
- **Con:** History and mobile push usually need a bouncer (ZNC); not product-grade moderation/SSO.
- **Con:** DCC file transfer bypasses the server — NAT and malware risk.

## Comparison
- vs Slack/Teams/Discord: those win for customer chat, SSO, and guaranteed history.
- vs [[webSocket]] product chat: WebSocket apps own the product UX; IRC is a shared public protocol.
- vs [[WebRTC]]: IRC is text; realtime A/V needs WebRTC.


### Use cases
- Open-source project chat, ops channels on Libera/OFTC, and bots that bridge C…

- **Example:** A deploy bot SASL-authenticates, joins `#ops`, and PRIVMSG’s rel…
