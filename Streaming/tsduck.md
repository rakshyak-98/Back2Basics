[[Streaming]] [[MPEG-TS]] [[IPTV]] [[ingestion]] [[Multicast]] [[flussonic]] [[CAS (Conditional Access System)]] [[demux]]

# tsduck

> TSDuck — CLI tools to capture, filter, and rewrite MPEG-TS (join multicast, zap a channel, analyze PIDs).

```txt
        tsduck ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk tsduck end-to-end

## Sources
- [Wikipedia — tsduck](https://en.wikipedia.org/wiki/tsduck) — overview

## Key Concepts
- **MPTS:** Many TV services in one TS — “One UDP flow carries a bouquet of channels.”
- **SPTS:** Single program TS — “Decoders often want one service per address.”
- **service_id:** Channel id in PAT/PMT — “zap picks the service_id, not a random PID.”
- **PAT:** Maps service → PMT PID — “Directory of programs in the multiplex.”
- **PMT:** Lists video/audio/PCR PIDs — “What to demux for this one channel.”
- **zap:** Extract one service cleanly

**Flow:**

1. **Join** — `-I ip` on the source multicast/unicast.
2. **Identify** — analyze PAT; pick `service_id`.
- **Note:** 3. **Zap** — `-P zap <service_id>` rebuilds PAT/PMT for that service.
- **Note:** 4. **Ship** — `-O ip` (or file) so each downstream gets an SPTS.

- **Note:** `-I ip` joins the MPTS source

[!NOTE]
- **Note:** Relevance to `zap`: the original PAT lists *all* MPTS services


- **Core:** An MPTS multiplexes many channels over one UDP/multicast flow. PAT maps `serv…

## Technical Details
```txt
MPTS multicast (many services)
      │
      ▼
tsp -I ip … -P zap <service_id> -O ip …
      │
      ▼
SPTS (one channel) + rebuilt PAT/PMT
```

```bash
# One channel: MPTS → SPTS
tsp -I ip <multicast_ip>:<port> \
    -P zap <service_id> \
    -O ip <output_ip>:<output_port>

# See what’s in the multiplex
tsp -I ip 239.1.1.1:5000 -P analyze -O drop
# or: tsp -I ip … -P until --seconds 5 -P tables -O drop
```

- Split many services (one `tsp` per `service_id`):

```bash
SRC="239.1.1.1:5000"
SERVICES=(101 102 103 104)
BASE_PORT=6001
for i in "${!SERVICES[@]}"; do
  PORT=$((BASE_PORT + i))
  tsp -I ip "$SRC" -P zap "${SERVICES[$i]}" \
      -O ip "239.2.2.$((i + 2)):${PORT}" &
done
wait
```

| Knob | Why it matters |
|------|----------------|
| `service_id` | Wrong id ⇒ silent wrong channel or empty SPTS |
| IGMP / interface | Must join on the correct NIC (`-I ip` options) |
| Output address/port | Collisions overwrite; one SPTS per dest |
| `analyze` / `tables` | Confirm PAT/PMT before automating zap maps |
| PCR / continuity | Zap should preserve continuity; watch CC errors |

- Debug: `tsp -P analyze` → match service_id → Wireshark UDP loss → compare bit…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| No packets out | Join / IGMP / firewall | Fix NIC, multicast route, allow UDP |
| Empty or black SPTS | service_id vs PAT | `analyze`; correct id; confirm PMT PIDs present |
| Downstream demux fails | Stale PAT copied | Use `zap` (rebuild SI), don’t raw PID filter only |
| CC errors / freezes | Loss on input multicast | Fix network; buffer; check source encoder |
| Wrong channel on port N | Map script off-by-one | Log service_id ↔ port; assert with analyze |
| Works for one, fails at scale | Too many tsp / CPU | Batch carefully; consider headend demux appliance |

- **Mistake:** **PID filter ≠ zap**
- **Mistake:** **service_id is not the LCN**
- **Mistake:** **One process per service is normal**
- **Mistake:** **Multicast TTL / scope**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Already SPTS from the encoder**
- **Con / skip when:** **OTT CMAF-only plant**
- **Con / skip when:** **One-off file remux with ffmpeg**
- **Con / skip when:** **You need full CAS headend control**

## Comparison
- vs [[HLS]]: **OTT CMAF-only plant**


### Use cases
- An MPTS multiplexes many channels over one UDP/multicast flow. PAT maps `serv…

- Used wherever tsduck sits in an ingest → package → CDN → player path
