[[System design]] [[API design]] [[Authentication web application]] [[cache system]] [[IM (Information Management) production systems]] [[KISS]] [[Streaming]]

# CMS (Content Management System)

> A CMS lets editors create, review, and publish structured content — headless systems expose JSON APIs while frontends own presentation.

```txt
        CMS (Content Manag ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Contrast headless vs monolithic CMS, publish→cache invalidation, and draft/pr…

## Sources
- Strapi / Directus documentation — headless content modeling — overview
- Jamstack architecture — decoupled content and delivery — overview

## Key Concepts
- **Headless:** content API + multi-channel clients.
- **Monolithic:** WordPress-style server-rendered sites.
- **Publish webhook:** bust Redis/CDN on publish.
- **Draft vs published:** tokenized preview; production filters `publish_at <= now`.

## Technical Details
```txt
Editors → admin UI → content API → apps / CDN / [[Streaming]] metadata
                │                    │
           workflow state      webhooks → cache invalidation
                │
           asset storage (object storage + CDN)
```

| Style | Examples | When |
|-------|----------|------|
| Headless | Strapi, Directus, Sanity | Multi-channel |
| Git-based | Markdown in repo | Dev-heavy docs |
| Monolithic | WordPress | Marketing SSR HTML |
| Broadcast MAM | Dalet, Avid | Pro video — [[IM (Information Management) production systems]] |

```json
{ "content_type": "movie", "fields": { "title": "string", "slug": "uid", "poster": "media", "publish_at": "datetime" } }
```

```txt
CMS publish → POST /internal/revalidate { slug }
→ delete Redis keys + CDN purge
```

- RBAC: author/editor/publisher.
- Separate preview credentials ([[Authentication web application]]).

| Symptom | Direction |
|---------|-----------|
| Stale after publish | Webhook / [[cache system]] invalidation missing |
| Draft public | Filter misconfiguration |
| Slow editor | Direct upload to object storage |

## Mistakes to Avoid
- **Mistake:** Hot-path clients hitting raw CMS instead of BFF/edge cache
- **Mistake:** Same API keys for preview and production
- **No purge webhook::** → editors “publish” into stale CDN

## Pros/Cons or Trade-offs
- **Headless pro:** channel flexibility; **con:** more moving parts.
- **Monolithic pro:** fast to ship a site; **con:** harder multi-app reuse.
- **Trade-off:** CMS vs Markdown-in-git ([[KISS]] for tiny blogs).

## Comparison
- vs [[IM (Information Management) production systems]]: broadcast MAM is specialized CMS for media…
- vs static generators: git content vs editorial workflows.


### Use cases
- Streaming title metadata, marketing sites, and multi-channel product catalogs.
