[[ingress]] [[Kubernetes services]] [[Configuration]] [[MQTT]] [[connection pooling]] [[WAL (Write-Ahead Log)]]

# HES Architecture

> A Head-End System (HES) sits at the edge of trust between devices and the core platform — ingesting telemetry, validating identity, buffering bursts, and forwarding with at-least-once delivery that the core must deduplicate.

---

## What "HES" means in practice

The acronym collides by industry:

| Domain | HES role |
|--------|----------|
| **Utilities / smart grid** | Meter data collection (DLMS/COSEM, IEC 61850 adapters) |
| **Healthcare** | Clinical edge gateway — protected health information boundary before cloud |
| **Generic IoT** | Device ingest tier with store-and-forward |

Confirm scope with stakeholders before designing — compliance and protocol adapters differ.

## Reference flow

```txt
Devices / clients
      ↓  (MQTT, HTTPS, batch files)
┌─────────────────────────────────────┐
│  Edge / HES tier                    │
│  authenticate → validate → buffer → route │
└──────────┬──────────────────────────┘
           ↓
    Core platform (cloud or on-premises)
    analytics · billing · electronic health record · supervisory control
```

**Non-functional targets** common to HES deployments:

- High availability at the edge cluster (often 99.9%+)
- At-least-once ingest with **idempotent core** writes
- Certificate-based device identity
- Store-and-forward when wide-area network is down
- Correlation identifiers in logs (device identifier, sequence)

## Kubernetes edge topology (example)

```txt
Edge cluster per region / substation / clinic
  DaemonSet: protocol adapter agents
  StatefulSet: local queue (Kafka, NATS JetStream) + deduplication store
  Deployment: HES application programming interface (validate, enrich, forward)
  Persistent volume: spool for outage hours

Cloud
  Ingest application programming interface + [[connection pooling]] to online transaction processing
  Stream processor for anomalies
  Object storage for cold archive
```

## Ingest contract

```http
POST /v1/readings
Authorization: Bearer <device JWT>
Idempotency-Key: <deviceId>:<sequence>
Content-Type: application/json

{ "deviceId", "ts", "metrics", "fwVersion" }
→ 202 Accepted + correlationId
```

Core database:

```sql
INSERT INTO readings (device_id, seq, ts, payload)
VALUES ($1, $2, $3, $4)
ON CONFLICT (device_id, seq) DO NOTHING;
```

## Edge proxy and health

[[Configuration]] example (nginx): rate limit per device, body size cap, read timeout aligned with upstream.

Kubernetes **readiness** should fail when local queue depth exceeds threshold or certificate expires within seven days — distinguish "alive" from "can forward."

## Failure modes

| Symptom | Direction |
|---------|-----------|
| Device retry storm | Scale HES pods; fix upstream 5xx; backoff in firmware |
| Duplicate billing reads | Enforce `(device_id, seq)` uniqueness |
| Edge disk full | Restore WAN; define reject versus drop policy before incident |
| Authentication spike | Certificate rotation; Network Time Protocol skew |
| Latency service level objective miss | Hot device partition — shard by device identifier |

*What breaks first during partition?* Spool disk without a defined overflow policy.

## Sources

- IEC 61968 / utility head-end integration guides (domain-specific).
- NIST SP 800-207 — zero trust at the edge (identity and policy).
- Kubernetes edge computing patterns — CNCF TAG Runtime.
