[[System design]] [[API design]] [[Authentication web application]] [[cache system]]

# CMS (Content Management System)

> Authoring + storage + delivery API for structured content — **headless** separates editorial from presentation.

---

## Mental model

A **CMS** lets non-engineers **create, edit, publish** content (pages, articles, video metadata, assets) with **workflow** (draft → review → live). **Headless CMS** exposes **JSON/API** only — web/mobile apps render UI; **monolithic CMS** (WordPress) renders HTML server-side.

```txt
Editors ──► CMS admin UI ──► content API ──► apps / CDN / [[Streaming]] metadata
                │                │
           workflow state    webhooks → rebuild cache
                │
           asset storage (S3 + CDN)
```

| Style | Examples | When |
|-------|----------|------|
| **Headless** | Strapi, Directus, Sanity | Multi-channel product |
| **Git-based** | Markdown in repo | Dev-heavy docs |
| **Broadcast MAM** | Dalet, Avid | Video IM systems — see [[IM (Information Management) production systems]] |

Streaming platforms use CMS for **title metadata, images, CID, geo rules** — playback still from origin/CDN.

---

## Standard config / commands

### Headless content model (example)

```json
{
  "content_type": "movie",
  "fields": {
    "title": "string",
    "slug": "uid",
    "synopsis": "richtext",
    "poster": "media",
    "content_id": "string",
    "drm_policy": "enum",
    "publish_at": "datetime"
  }
}
```

### API consumption pattern

```txt
GET /api/movies?filters[published_at][$lte]=now&populate=poster
Cache at CDN with short TTL + purge webhook on publish
Client apps never hit CMS directly in prod — BFF or edge cache
```

### Webhook on publish → cache bust

```txt
CMS publish event → POST /internal/revalidate { slug: "movie-123" }
→ delete Redis keys + CDN purge API
→ optional static rebuild (SSG)
```

### Draft vs preview

```txt
Preview: tokenized URL with draft API key — no CDN cache
Production: only status=published && publish_at <= now
```

### Asset pipeline

```txt
Upload poster → CMS → S3 → img CDN (resize variants)
Video files usually NOT in CMS blob — store URL + CID to origin packager
```

### RBAC for editorial

```txt
Roles: author, editor, legal, admin
Field-level: drm_policy editable only by admin
Audit log: who published what when (compliance)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Site shows old title | CDN/API cache | Purge; webhook on publish |
| Draft visible publicly | Preview key leaked | Separate preview domain |
| Missing poster | Media not populated | `populate=*` or explicit join |
| Slug collision | Unique constraint | Enforce at CMS |
| Streaming CID mismatch | Manual typo | Validation regex; golden CID registry |
| Editor timeout on upload | Large video in CMS | External asset URL only |
| Webhook 500 loop | Downstream revalidate | Idempotent webhook handler |

---

## Gotchas

> [!WARNING]
> **Rich text XSS** — sanitize HTML from CMS before render.

> [!WARNING]
> **CMS as system of record for entitlements** — playback auth belongs in subscription service, not CMS field.

> [!WARNING]
> **Locale explosion** — N languages × M fields — plan fallback locale strategy.

> [!WARNING]
> **Hard-coded content IDs in app** — use slug/API; store mapping in CMS.

> [!WARNING]
> **No publish schedule timezone** — UTC vs local launch bugs.

---

## When NOT to use

- **Hardcoded marketing one-pager** — git + MD faster.
- **Transactional order data** — CMS for editorial; orders in OLTP DB.
- **Real-time chat** — not CMS domain.

---

## Related

[[System design]] [[API design]] [[cache system]] [[IM (Information Management) production systems]] [[Compliance Reporting to Broadcasters]] [[Streaming]]
