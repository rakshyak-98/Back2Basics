[[NAT (Network Address Translation)]] [[webSocket]] [[TCP]] [[UDP]] [[Streaming]]

# SIP (Session Initiation Protocol)

> VoIP/media signaling — REGISTER, INVITE, RTP path setup, NAT debugging for streaming engineers — **RFC 3261 ops view**.

---

## Mental model

**SIP** is text-based signaling (like HTTP) for establishing, modifying, and tearing down **media sessions**. Actual audio/video flows over **RTP/RTCP** (usually UDP) on separate ports — SIP only negotiates codecs and endpoints.

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

| Message | Role |
|---------|------|
| **REGISTER** | Bind AOR (`sip:user@domain`) to contact URI (IP:port) |
| **INVITE** | Start session; body carries **SDP** (codecs, ports) |
| **ACK** | Confirm 200 OK to INVITE |
| **BYE** | Hang up |
| **OPTIONS** | Capability ping |

**SDP offer/answer** lists `m=audio PORT RTP/AVP` — if NAT wrong, signaling succeeds but **one-way audio** (classic production bug).

---

## Standard config / commands

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

Enable **SIP decoding** + **RTP stream analysis** (Telephony → RTP streams).

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

---

## Triage (when things break)

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

---

## Gotchas

> [!WARNING]
> **SIP ALG on consumer routers** — mangled headers; disable ALG industry-wide recommendation.

> [!WARNING]
> **Private IP in SDP** — remote sends RTP to unroutable 10.x address.

> [!WARNING]
> **TLS/SRTP vs plain** — WebRTC requires DTLS-SRTP; legacy SIP trunk may be RTP only — transcoding/SBC boundary.

> [!WARNING]
> **Re-INVITE for hold/music** — missed re-INVITE handling → dropped call on hold.

> [!WARNING]
> **Registration expiry** — NAT binding dies before re-REGISTER; shorten expiry or keepalive OPTIONS.

---

## When NOT to use

- **Low-latency game state** — use custom UDP or [[webSocket]], not SIP.
- **One-to-many broadcast** — RTMP/HLS/SRT stack; SIP is session-oriented.
- **DIY SIP without SBC at scale** — toll fraud scanning hits port 5060 constantly.

---

## Related

[[NAT (Network Address Translation)]] [[TCP]] [[Streaming]] [[webSocket]] [[DNS]]
