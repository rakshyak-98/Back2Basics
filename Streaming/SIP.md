[[NAT (Network Address Translation)]] [[webSocket]] [[TCP]] [[UDP]] [[Streaming]] [[DNS]]

# SIP (Session Initiation Protocol)

> SIP (Session Initiation Protocol) — SIP is text-based signaling (like HTTP) for establishing, modifying, and tearing down media sessions. Actual audio/video flows over RTP/RTCP (usually UDP)

```txt
        SIP (Session Initi ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about SIP to see if you understand the pipeline role, failur…

## Sources
- [Wikipedia — SIP](https://en.wikipedia.org/wiki/SIP) — overview
- [RFC 3261 — SIP](https://datatracker.ietf.org/doc/html/rfc3261) — deep-dive

## Key Concepts
- **Note:** **SIP** is text-based signaling (like HTTP) for establishing, modifying, and …

| Message | Role |
|---------|------|
| **REGISTER** | Bind AOR (`sip:user@domain`) to contact URI (IP:port) |
| **INVITE** | Start session; body carries **SDP** (codecs, ports) |
| **ACK** | Confirm 200 OK to INVITE |
| **BYE** | Hang up |
| **OPTIONS** | Capability ping |

- **Note:** **SDP offer/answer** lists `m=audio PORT RTP/AVP`

## Technical Details
```txt
Phone/UAC                    SIP Proxy/PBX                    Phone/UAS
   │── REGISTER ─────────────►│                               │
   │◄── 200 OK ────────────────│                               │
   │── INVITE (SDP offer) ─────►│── INVITE ────────────────────►│
   │◄── 180 Ringing ────────────│◄── 180 ───────────────────────│
   │◄── 200 OK (SDP answer) ────│◄── 200 ───────────────────────│
   │── ACK ────────────────────►│                               │
   │════════ RTP audio/video (direct or via media relay) ═══════│
   │── BYE ────────────────────►│                               │
```

### Minimal INVITE flow (debug with sipsak)

```shell
# OPTIONS ping
sipsak -s sip:server.example.com -v

# REGISTER (needs credentials on real PBX)
# Use pjsua, linphone, or Asterisk CLI for full tests
```

### Asterisk / FreeSWITCH quick checks

```shell
# Asterisk
asterisk -rx "sip show peers"
asterisk -rx "pjsip show endpoints"
asterisk -rvvv   # verbose SIP trace

# FreeSWITCH
fs_cli -x "sofia status profile internal reg"
fs_cli -x "sofia global siptrace on"
```

### Wireshark filters

```txt
sip || rtp
sip.Method == "INVITE"
sip.Call-ID == "abc@host"
```

- Enable **SIP decoding** + **RTP stream analysis** (Telephony → RTP streams).

### NAT traversal toolkit

| Mechanism | Fixes |
|-----------|-------|
| **STUN** | Client learns public IP:port |
| **TURN** | Media relay when direct RTP blocked |
| **ICE** | Candidate pairing (WebRTC) |
| **RTP ALG** | Router SIP helper — often **breaks** SIP; disable and use proper edge SBC |
| **SBC** | Session border controller — normalizes SIP/RTP at network edge |

```txt
Contact header must reflect reachable address:
  Contact: <sip:user@203.0.113.5:5060>   ; public, not 192.168.1.10
SDP c= line must match RTP port forwarding / media relay
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Registers but no audio | RTP flow in Wireshark | NAT: fix Contact/SDP; enable TURN/media relay |
| One-way audio | Compare both directions RTP | Firewall UDP range; asymmetric NAT |
| 408 / timeout | Routing DNS SRV `_sip._udp.domain` | DNS [[DNS]] SRV/A; firewall 5060 UDP/TCP |
| 401 loop | Auth realm, wrong password | Align digest creds; clock skew (NTP) |
| Works on LAN, fails mobile | Carrier CGNAT | TURN mandatory |
| 488 Not Acceptable | Codec mismatch in SDP | Transcode at SBC or align G.711/Opus |
| Calls drop at 32s | RTP timeout, no keepalive | Session timers; send RTP comfort noise |

```shell
# RTP port range (open on firewall)
# Asterisk default rtp.conf: 10000-20000/udp
ss -ulnp | grep -E '5060|10000'
```

- **Mistake:** **SIP ALG on consumer routers**
- **Mistake:** **Private IP in SDP**
- **Mistake:** **TLS/SRTP vs plain**
- **Re-INVITE for hold/music**::** → dropped call on hold
- **Mistake:** **Registration expiry**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Low-latency game state**
- **Con / skip when:** **One-to-many broadcast**
- **Con / skip when:** **DIY SIP without SBC at scale**

## Comparison
- vs [[webSocket]]: **Low-latency game state** — use custom UDP or [[webSocket]], not SIP.


### Use cases
- Used wherever SIP sits in an ingest → package → CDN → player path
