[[Streaming]] [[DRM]] [[CMS]] [[database sharding]]

# Compliance Reporting to Broadcasters

> Auditable reconciliation of entitlements + consumption → licensed Content IDs — **rights / royalty enforcement**, not analytics vanity metrics.

---

## Mental model

**Compliance reporting** is the **contractual data pipeline** that proves how licensed content was **sold, entitled, and consumed** per **Content ID (CID)** and **Broadcaster Network ID**. Studios and rights holders use it for **revenue share, minimum guarantees, and geo/format restrictions**. Errors become legal exposure — design for **immutability, idempotency, and late-arriving data**.

```txt
Billing (subs/PPV) ──► Entitlement ledger ──► Playback beacons
        │                      │                      │
        └──────────► Reconciliation job ◄──────────────┘
                           │
                    Compliance report (CSV/API)
                           │
                    Broadcaster / licensor SFTP
```

| Data source | Proves | Typical grain |
|-------------|--------|---------------|
| **Subscription/transaction** | Who paid, when, plan | Order ID, user hash, SKU |
| **Entitlement grant** | Right to play title X | CID, window start/end, geo |
| **Consumption telemetry** | Actual plays | CID, start/end, device, territory |
| **Ad insertion (optional)** | Commercial obligations | SCTE-35, pod position |

Reports must **join on stable IDs** — internal UUIDs useless to licensor; map to **canonical CID** at ingest ([[CMS]] metadata).

---

## Standard config / commands

### Minimum report schema (negotiate per contract)

```txt
Field                  Example                    Notes
report_period          2026-07-01/2026-07-31      UTC boundaries in contract
broadcaster_id         NET-UK-001                 Licensor-assigned
content_id             CID-MOVIE-8842             Canonical, not internal slug
territory              GB                         ISO 3166-1
delivery_format        HLS_DASH_DRM               As licensed
transaction_type       SVOD|PAYG|FREE_TRIAL
unique_viewers         12847                      Method defined in contract
total_minutes_viewed   892341                     ≥ completed % threshold?
revenue_share_basis    45231.18                   Currency + tax rules
```

### Pipeline checklist

```txt
1. Idempotent ingest — event_id dedupe (at-least-once Kafka OK)
2. Immutable raw store — append-only (S3 + WORM / Glacier lock)
3. Late events window — re-open daily partition T+7 common
4. Clock — all timestamps UTC; document DST handling
5. PII — hash subscriber IDs; never ship emails unless contracted
6. Sign/export — GPG to SFTP; checksum file alongside CSV
```

### Example daily reconciliation SQL sketch

```sql
-- Consumption joined to entitlement for licensed window
SELECT c.content_id, c.territory,
       COUNT(DISTINCT c.user_hash) AS unique_viewers,
       SUM(c.watch_seconds) / 60.0 AS total_minutes
FROM consumption_events c
JOIN entitlement_grants e
  ON c.content_id = e.content_id AND c.user_hash = e.user_hash
WHERE c.event_time >= e.window_start AND c.event_time < e.window_end
  AND c.event_date = '2026-07-22'
GROUP BY 1, 2;
```

### Export job (ops)

```bash
# Signed export to licensor drop zone
aws s3 cp s3://compliance-reports/daily/2026-07-22/report.csv.gpg s3://licensor-inbound/ --sse AES256
sha256sum report.csv.gpg > report.csv.gpg.sha256
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Licensor rejects report | Schema version drift | Pin contract appendix; validation gate before export |
| Minutes > physical possible | Duplicate beacons | Dedupe on `(session_id, heartbeat_seq)` |
| Missing territory | GeoIP default wrong | Require CDN-Country header; fail closed |
| Free trial counted as paid | transaction_type mapping | Business rules table per SKU |
| Late Kafka events | Partition reprocessing | Re-run reconciliation for open window |
| CID mismatch | CMS typo vs ingest | Golden CID registry; block publish without CID |

---

## Gotchas

> [!WARNING]
> **Analytics ≠ compliance** — QoE dashboards use sampled data; compliance needs **complete, auditable** counts.

> [!WARNING]
> **Rewound VOD scrubbing** — contract may count **unique completion %** not raw heartbeats.

> [!WARNING]
> **DRM offline downloads** — plays offline may batch-upload; reporting lag must be disclosed.

> [!WARNING]
> **Multi-CDN duplicate segments** — count **unique viewer sessions**, not segment requests.

> [!WARNING]
> **Manual CSV edits** — breaks audit trail; regenerate from immutable raw only.

---

## When NOT to use

- **Internal product analytics** — use warehouse/BI stack; don't overload compliance schema.
- **Pre-revenue MVP** — still **log raw events** early; retrofitting CIDs is painful.
- **Real-time licensor API before legal requires it** — batch daily/weekly unless contract mandates SLA.

---

## Related

[[Streaming]] [[CMS]] [[DRM]] [[ingestion]] [[Microservice]] [[database sharding]]
