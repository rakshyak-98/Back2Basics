[[System design]] [[API design]] [[Authentication web application]] [[cache system]] [[IM (Information Management) production systems]]

# CMS (Content Management System)

> A content management system lets editors create, review, and publish structured content — headless systems expose JSON application programming interfaces while frontends and applications own presentation.

---

## Headless versus monolithic

```txt
Editors → admin user interface → content API → applications / CDN / [[Streaming]] metadata
                │                    │
           workflow state      webhooks → cache invalidation
                │
           asset storage (object storage + CDN)
```

| Style | Examples | When |
|-------|----------|------|
| Headless | Strapi, Directus, Sanity | Multi-channel product (web, mobile, television) |
| Git-based | Markdown in repository | Developer-heavy documentation |
| Monolithic | WordPress | Marketing site with server-rendered HTML |
| Broadcast media asset management | Dalet, Avid | Professional video — [[IM (Information Management) production systems]] |

Streaming products use content management for **title metadata, posters, content identifiers, geo rules** — playback still comes from origin or content delivery network.

## Content model (example)

```json
{
  "content_type": "movie",
  "fields": {
    "title": "string",
    "slug": "uid",
    "synopsis": "richtext",
    "poster": "media",
    "content_id": "string",
    "publish_at": "datetime"
  }
}
```

## Consumption pattern

```txt
GET /api/movies?filters[published_at][$lte]=now&populate=poster
Cache at CDN with short time-to-live + purge webhook on publish
Production clients hit backend-for-frontend or edge cache — not raw content management in hot path
```

### Publish webhook → cache bust

```txt
CMS publish → POST /internal/revalidate { slug: "movie-123" }
→ delete Redis keys + CDN purge
→ optional static site regeneration
```

### Draft versus preview

Preview uses tokenized draft application programming interface key — no CDN cache. Production serves only `status=published` and `publish_at <= now()`.

## Authorization

Role-based access: author, editor, publisher. Separate preview credentials from production keys ([[Authentication web application]]).

## Common failures

| Symptom | Direction |
|---------|-----------|
| Stale content after publish | Webhook or [[cache system]] invalidation missing |
| Draft visible publicly | Filter misconfiguration |
| Slow editor | Large media through wide-area network — direct upload to object storage |

*When would you skip a content management system?* Single developer blog — Markdown in git may suffice ([[KISS]]).

## Sources

- Strapi / Directus documentation — headless content modeling.
- Jamstack architecture — decoupled content and delivery.
