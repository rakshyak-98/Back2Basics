[[CMS]] [[Streaming]] [[Compliance Reporting to Broadcasters]] [[transcoding]] [[DRM]] [[System design]]

# IM (Information Management) production systems

> Broadcast Information Management combines Media Asset Management with workflow orchestration — canonical masters, rights metadata, and frame-accurate lineage feeding playout and over-the-top streaming.





## Interview Relevance
Map MAM/PAM pieces: ingest, metadata, workflow, playout — and where broadcast differs from generic CMS.

## Sources
- EBU Core Metadata — broadcast interoperability — overview
- AMWA NMOS — networked media for professional facilities — overview
- SMPTE standards — timecode and material exchange formats — overview

## Key Concepts
- **MAM/PAM:** media/production asset management for broadcast workflows.
- **Ingest → metadata → workflow → playout:** the production pipeline.
- **Rights and versions:** edit decision lists, proxies, and air dates.
- **Not a blog CMS:** professional media ops constraints.

## Technical Details
### IM versus web content management

[[CMS]] products optimize for web pages and marketing content. **Information Management** in broadcast handles professional formats (Material Exchange Format, General Exchange Format), **timecode**, frame-accurate edits, and **rights windows** — the system of record for what may air or stream where.

```txt
Ingest (tape, file, live) → IM catalog → edit / approve → transcode → [[Streaming]] / playout
                │                │
           metadata hub     compliance export
                │
           Archive (cold storage + proxy)
```

| Component | Role | Vendor examples |
|-----------|------|-----------------|
| Media Asset Management | Master storage + metadata | Dalet, Avid, CatDV |
| Production Asset Management | Editing projects | Avid, Adobe |
| Workflow engine | Review, legal, quality control states | Custom, Business Process Model and Notation |
| Proxy | Low-resolution edit preview | H.264 mezzanine |
| Playout | Linear channel automation | Harmonic, Pebble |

Over-the-top products often **sync** approved assets to a product [[CMS]] — Information Management remains authoritative for masters and rights.

### Metadata model (broadcast)

```txt
Content_ID (CID)     — licensor canonical identifier
House_ID             — internal unique key
Title / episode / season
Rights: territory, window_start, window_end, exclusivity
Technical: format, duration, timecode_start, audio layout
Lineage: source version, parent_asset_id
```

Link [[Compliance Reporting to Broadcasters]] exports to Content_ID for royalty and play logs.

### Typical workflow

```txt
REGISTERED → QC → LEGAL_CLEAR → APPROVED → PUBLISHED → ARCHIVED
```

On **APPROVED**: push mezzanine to object storage, trigger adaptive bitrate transcode ([[transcoding]]), write consumer-facing metadata, enable entitlement, register [[DRM]] policy.

Editors work on **proxy** files; masters stay on nearline storage — editing masters over wide-area network destroys user experience.

### Operational failures

| Symptom | Likely cause |
|---------|--------------|
| Streamable asset missing in app | Content management sync lag from Information Management webhook |
| Wrong episode on air | Playout schedule bound to outdated version |
| Rights violation | `window_end` passed without automated unpublish |
| Slow editor | Master pulled over network instead of proxy |

Information Management is not the player hot path — export identifiers and URLs to low-latency services.

## Real-World Applications
Broadcast networks, post-production houses, and streaming original content factories.

## Pros/Cons or Trade-offs
- **Pro:** End-to-end media lifecycle with audit.
- **Con:** Heavyweight integrations; vendor lock-in risk.
- **Trade-off:** suite platforms vs best-of-breed tools.

## Comparison
- vs [[CMS]]: editorial web CMS vs broadcast-grade media asset systems.
- vs [[on-demand vs static file (Streaming)]]: IM feeds what streaming publishes.

## Mistakes to Avoid
- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.
