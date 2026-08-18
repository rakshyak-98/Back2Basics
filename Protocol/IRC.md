[[Protocol]] [[TCP]]

# IRC

> IRC (Internet Relay Chat) — clients join a server (or network of servers) for channels and DMs; text chat over a simple TCP protocol.

## Mental model

**Say it in one breath:** You connect a client to an IRC server, join `#channels`, and messages fan out through the network — group chat by design, with optional private messages and file DCC.

```txt
Client ──TCP 6667/6697──► IRC server ◄──► other servers (same network)
                              │
                         #channel / PRIVMSG
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Network** | Linked IRC servers that share state | “Libera / OFTC are networks, not one box.” |
| --- | --- | --- |
| **Channel** | Named room (`#ops`) | “Channels are the group forums.” |
| **Nick** | Your display identity on the network | “Nick collisions and services (NickServ) matter.” |
| **PRIVMSG** | Message to a nick or channel | “All chat is PRIVMSG under the hood.” |
| **IRCv3** | Modern extensions (CAP, SASL, batches) | “Real clients negotiate capabilities, not raw RFC only.” |

### How the story goes

1. Client opens TCP (often TLS on 6697).
2. Registers nick, optional SASL/NickServ authentication.
3. `JOIN #channel` → receives traffic for that room.
4. operations moderate with modes (`+o`, bans); services handle accounts.

## Standard config / commands

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

| 6667 vs 6697 | Plain vs TLS — corporate and public nets expect TLS |
| --- | --- |
| SASL | Auth before join — required on many networks |
| Flood limits | Bots without rate limits get KLINE’d |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Connect timeout | DNS / firewall / wrong port | Try 6697 TLS; whitelist IRC ports |
| Nick in use | Collision / ghost session | Ghost via NickServ; pick unique nick |
| Can’t join channel | Ban / +i / +k key | Ask ops; check `MODE #chan` |
| Silent after connect | Need CAP/SASL or registration | Enable SASL; identify before JOIN |
| Bot banned for flood | Burst PRIVMSG | Pace messages; use server-side limits |
| Split / missing users | Net split between servers | Wait for sync; check network status |

## Gotchas

> [!WARNING]
> **Plaintext IRC still exists** — treat 6667 as debug only; credentials and chat leak on the wire.

> [!WARNING]
> **Services ≠ the IRC daemon** — NickServ/ChanServ are separate; misconfigured linking looks like “auth broken.”

> [!WARNING]
> **DCC file transfer bypasses the server** — peer-to-peer; NATs and malware risk apply.

## When NOT to use

- **Product chat for customers** — use Slack/Teams/Discord APIs with moderation and SSO.
- **Guaranteed mobile push + history** — IRC history is client-dependent unless you add a bouncer (ZNC).
- **Binary realtime media** — use [[WebRTC]], not IRC.

## Related

[[Protocol]] [[TCP]] [[webSocket]] [[WebRTC]] [[SOCKS (Socket Secure)]]
