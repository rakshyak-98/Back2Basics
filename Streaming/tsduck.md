[[Streaming]] [[MPEG-TS]] [[IPTV]] [[ingestion]] [[Multicast]]

# tsduck

> TSDuck — CLI tools to capture, filter, and rewrite MPEG-TS (join multicast, zap a channel, analyze PIDs).

---

## Mental model

**Say it in one breath:** `tsp` is a plugin pipeline — input a transport stream, run filters, output another stream or analysis.

```txt
MPTS multicast (many services)
      │
      ▼
tsp -I ip … -P zap <service_id> -O ip …
      │
      ▼
SPTS (one channel) + rebuilt PAT/PMT
```

`-I ip` joins the MPTS source. `zap` keeps that service’s PIDs and rebuilds a clean PAT/PMT for one channel. `-O ip` sends the SPTS to its own multicast address/port.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MPTS** | Many TV services in one TS | “One UDP flow carries a bouquet of channels.” |
| **SPTS** | Single program TS | “Decoders often want one service per address.” |
| **service_id** | Channel id in PAT/PMT | “zap picks the service_id, not a random PID.” |
| **PAT** | Maps service → PMT PID | “Directory of programs in the multiplex.” |
| **PMT** | Lists video/audio/PCR PIDs | “What to demux for this one channel.” |
| **zap** | Extract one service cleanly | “Filter + rewrite SI so the SPTS is self-consistent.” |

### How the story goes (4 steps)

1. **Join** — `-I ip` on the source multicast/unicast.
2. **Identify** — analyze PAT; pick `service_id`.
3. **Zap** — `-P zap <service_id>` rebuilds PAT/PMT for that service.
4. **Ship** — `-O ip` (or file) so each downstream gets an SPTS.

> [!NOTE]
> Relevance to `zap`: the original PAT lists *all* MPTS services. After extract, that PAT is wrong. `zap` regenerates PAT/PMT so the output is a valid one-service stream.

> [!INFO]
> An MPTS multiplexes many channels over one UDP/multicast flow. PAT maps `service_id` → PMT PID; each PMT lists that channel’s elementary PIDs.

---

## Standard config / commands

```bash
# One channel: MPTS → SPTS
tsp -I ip <multicast_ip>:<port> \
    -P zap <service_id> \
    -O ip <output_ip>:<output_port>

# See what’s in the multiplex
tsp -I ip 239.1.1.1:5000 -P analyze -O drop
# or: tsp -I ip … -P until --seconds 5 -P tables -O drop
```

Split many services (one `tsp` per `service_id`):

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

Debug: `tsp -P analyze` → match service_id → Wireshark UDP loss → compare bitrate in versus out.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No packets out | Join / IGMP / firewall | Fix NIC, multicast route, allow UDP |
| Empty or black SPTS | service_id vs PAT | `analyze`; correct id; confirm PMT PIDs present |
| Downstream demux fails | Stale PAT copied | Use `zap` (rebuild SI), don’t raw PID filter only |
| CC errors / freezes | Loss on input multicast | Fix network; buffer; check source encoder |
| Wrong channel on port N | Map script off-by-one | Log service_id ↔ port; assert with analyze |
| Works for one, fails at scale | Too many tsp / CPU | Batch carefully; consider headend demux appliance |

---

## Gotchas

> [!WARNING]
> **PID filter ≠ zap** — dropping PIDs without rewriting PAT/PMT leaves a lying directory; many decoders choke.

> [!WARNING]
> **service_id is not the LCN** — logical channel numbers in NIT/SDT are a different label. Zap wants the PAT service_id.

> [!WARNING]
> **One process per service is normal** — sharing one tsp incorrectly is a common footgun; separate outputs are clearer.

> [!WARNING]
> **Multicast TTL / scope** — output SPTS may never leave the host subnet if TTL/routing is wrong.

---

## When NOT to use

- **Already SPTS from the encoder** — no zap needed; just ingest.
- **OTT CMAF-only plant** — you’re in [[HLS]]/[[DASH]] land; TSDuck is for [[MPEG-TS]] plants.
- **One-off file remux with ffmpeg** — fine for VOD files; TSDuck shines on live TS + SI.
- **You need full CAS headend control** — vendor scrambler/CAS tools, not only tsp plugins.

---

## Related

[[MPEG-TS]] [[IPTV]] [[Multicast]] [[ingestion]] [[flussonic]] [[CAS (Conditional Access System)]] [[demux]]
