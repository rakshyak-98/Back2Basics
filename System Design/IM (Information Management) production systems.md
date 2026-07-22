[[CMS]] [[Streaming]] [[System design]] [[Compliance Reporting to Broadcasters]]

# IM (Information Management) production systems

> Enterprise MAM/PAM for broadcast — **metadata, workflow, and asset lifecycle** from ingest to playout and compliance.

---

## Mental model

**Information Management (IM)** in broadcast is **Media Asset Management (MAM)** plus **workflow orchestration**: log content, attach **metadata/CIDs**, manage **versions/rights**, route through **edit/approval**, and feed **playout/streaming** endpoints. Unlike a web **[[CMS]]**, IM systems handle **professional formats** (MXF, GXF), **timecode**, **frame-accurate edits**, and **rights windows**.

```txt
Ingest (tape/file/live) ──► IM catalog ──► edit/approve ──► transcode ──► [[Streaming]]/playout
                │                │
           metadata hub     compliance export
                │
           Archive (cold storage + proxy)
```

| Component | Role | Examples |
|-----------|------|----------|
| **MAM** | Asset storage + metadata | Dalet, Avid, CatDV |
| **PAM** | Production editing projects | Avid, Adobe prod |
| **Workflow engine** | State machine (review/legal) | Custom + BPMN |
| **Proxy** | Low-res edit preview | H.264 mezzanine |
| **Playout** | Linear channel automation | Harmonic, Pebble |

OTT stacks often **integrate** IM → export CID + mezzanine URL to product CMS — IM remains **system of record** for masters.

---

## Standard config / commands

### Core metadata model (broadcast)

```txt
Content_ID (CID)        Licensor canonical ID — [[Compliance Reporting to Broadcasters]]
House_ID                Internal unique
Title / Episode / Season
Rights: territory, window_start, window_end, exclusivity
Technical: format, duration, timecode_start, audio_layout
Lineage: source, version, parent_asset_id
```

### Typical workflow states

```txt
REGISTERED → QC → LEGAL_CLEAR → APPROVED → PUBLISHED → ARCHIVED
Reject loops: QC_FAIL → fix re-ingest
Hooks: webhook to transcode farm when APPROVED
```

### Integration to streaming pipeline

```txt
IM APPROVED event:
  1. Push mezzanine to object storage
  2. Trigger ABR transcode ([[transcoding]])
  3. Write CMS record (poster, synopsis, CID)
  4. Enable entitlement in subscription service
  5. Register DRM policy ([[DRM]])
```

### Proxy vs master policy

```txt
Editors work on proxy (720p H.264)
Master: ProRes/MXF on nearline storage
Never edit on master over WAN — local cache or proxy
```

### Search & discovery

```txt
Index: title, CID, tags, rights_end > now()
Faceted search for ops — "expiring rights in 30 days"
```

### Audit / compliance

```txt
Immutable audit: who changed rights window
Export play logs joined on CID — see [[Compliance Reporting to Broadcasters]]
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Streamable but not in app | CMS sync lag | Replay IM→CMS webhook |
| Wrong episode airs | Playout schedule vs IM version | Lock version on schedule bind |
| Transcode from old master | Wrong asset linked | Version pin in workflow |
| Rights violation | window_end passed | Automated unpublish job |
| Proxy/master mismatch | Re-ingest incomplete | QC gate block publish |
| Duplicate CID | Ingest without dedupe | Unique constraint on CID |
| Slow editor UX | Master over network | Force proxy workflow |

---

## Gotchas

> [!WARNING]
> **IM as playback database** — high-latency MAM queries don't belong in player hot path.

> [!WARNING]
> **Manual metadata entry** — typo CIDs break royalty reports; validate against licensor feed.

> [!WARNING]
> **Timecode vs stream offset** — ad insertion SCTE-35 needs frame-accurate IM markers.

> [!WARNING]
> **Archive tape recall latency** — cold storage restore hours; plan publish SLA.

> [!WARNING]
> **Parallel CMS + IM truth** — pick system of record per field; sync direction documented.

---

## When NOT to use

- **Creator UGC platform** — lightweight object storage + CMS beats Dalet-scale IM.
- **Simple podcast host** — audio CMS sufficient.
- **Real-time clip sharing** — IM workflow too slow; separate short-form pipeline.

---

## Related

[[CMS]] [[Streaming]] [[Compliance Reporting to Broadcasters]] [[transcoding]] [[DRM]] [[System design]]
