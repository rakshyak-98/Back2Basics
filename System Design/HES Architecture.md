[[System Design]] [[ingress]] [[Kubernetes services]] [[Configuration]] [[Epoll]]

# HES Architecture

> **HES** acronym is ambiguous in this vault (no prior mentions) — commonly **Home Energy System**, **Head-End System** (utilities/AMI), or **Health Examination System**. Below: **high-availability edge service** pattern applicable to meter gateways, clinic edge nodes, or IoT aggregators — define your domain acronym in the project README.

---

## Mental model

```txt
Devices / Clients
      ↓  (MQTT/HTTPS/batch)
┌─────────────────────────────────────┐
│  Edge / HES tier                    │
│  ingest → validate → buffer → route │
└──────────┬──────────────────────────┘
           ↓
    Core platform (cloud/on-prem)
    analytics · billing · EHR · SCADA
```

**HES role:** sit at the **edge of trust** — authenticate devices, normalize payloads, absorb burst traffic, survive upstream outages, never lose acknowledged reads.

**Typical non-functional reqs:**
- 99.9%+ availability at edge cluster
- At-least-once ingest with idempotent core
- Certificate-based device identity
- Store-and-forward when WAN down
- Observability with device correlation id

If your HES = **utility head-end:** add protocol adapters (DLMS/COSEM, IEC 61850). If **health edge:** PHI encryption, audit, HIPAA boundary before cloud.

---

## Standard config / commands

### Reference topology (K8s edge + cloud)

```txt
Edge cluster (per region / substation / clinic)
  - DaemonSet: protocol adapter agents
  - StatefulSet: local queue (Kafka/NATS JetStream) + Redis dedupe
  - Deployment: HES API (validate, enrich, forward)
  - PVC: spool for WAN outage (hours not days)

Cloud
  - Ingest API + [[connection pooling]] to OLTP
  - Stream processor (Flink/ksql) for anomalies
  - Cold storage (S3 + parquet)
```

### Ingest API contract

```http
POST /v1/readings
Authorization: Bearer <device JWT>
Idempotency-Key: <deviceId>:<sequence>
Content-Type: application/json

{ "deviceId", "ts", "metrics", "fwVersion" }
→ 202 Accepted + correlationId
```

### Idempotent write (core DB)

```sql
INSERT INTO readings (device_id, seq, ts, payload)
VALUES ($1, $2, $3, $4)
ON CONFLICT (device_id, seq) DO NOTHING;
```

### Health checks

```yaml
# k8s probes — distinguish "alive" vs "can reach cloud"
livenessProbe:  /healthz
readinessProbe: /ready  # fails if local queue > threshold OR cert expiry < 7d
```

### Nginx edge proxy ([[Configuration]])

```nginx
location /v1/ {
  proxy_pass http://hes-api;
  proxy_read_timeout 30s;
  client_max_body_size 1m;
  limit_req zone=device burst=20 nodelay;
}
```

### Observability minimum

```txt
Metrics: ingest_rate, queue_depth, forward_lag_seconds, device_auth_failures
Logs:    correlationId, deviceId (not PII payload)
Traces:  edge → cloud ingest span
Alerts:  queue_depth high 15m, cert expiry 14d
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Devices retry storm | 5xx rate, timeout | Scale HES pods; extend adapter backoff; fix DB pool |
| Duplicate readings in billing | Idempotency key | Enforce (device_id, seq) unique; audit adapter gen |
| Edge disk full | Spool PVC usage | Increase retention policy; restore WAN; drop policy w/ audit |
| Auth failures spike | Cert rotation | Push new device certs; check clock skew (NTP) |
| Cloud sees gaps | forward_lag metric | Network partition — expected; backfill from spool |
| Latency SLO miss | Hot partition device | Shard by deviceId; async pipeline |
| "HES" means different thing per team | Glossary | Rename service in docs; link domain spec |

---

## Gotchas

> [!WARNING]
> **At-least-once everywhere** — without idempotent core, duplicates become revenue or clinical errors.

> [!WARNING]
> **Edge clock drift** — device timestamps untrusted; record server ingest time separately.

> [!WARNING]
> **Full disk on spool** — define drop vs reject policy **before** incident; regulators may require no silent loss.

> [!WARNING]
> **Acronym collision** — confirm with stakeholders: Energy HES ≠ Hospital HES compliance scope.

---

## When NOT to use

- **Direct device-to-cloud only** — no outage buffer; fine for low-value telemetry, not billing/medical grade.
- **Monolith ingest in single VM** — first WAN blip becomes data loss without queue.
- **Custom binary protocol without schema registry** — versioning hell at 10k firmware variants.

---

## Related

[[ingress]] · [[Kubernetes services]] · [[MQTT]] · [[connection pooling]] · [[WAL (Write-Ahead Log)]] · [[half-open connections]] · [[Mermaid (DSL)]]
