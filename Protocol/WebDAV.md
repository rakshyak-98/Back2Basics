[[HTTP module]] [[TLS (Transport Layer Security)]] [[TCP]]

# WebDAV

> WebDAV extends HTTP with authoring methods so clients can manage files on a remote server — CalDAV and CardDAV reuse the same MOVE/COPY/PROPFIND primitives.

```txt
        WebDAV ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use WebDAV to check HTTP method literacy beyond GET/POST and to …

## Sources
- [RFC 4918 — HTTP Extensions for WebDAV](https://datatracker.ietf.org/doc/html/rfc4918) — deep-dive
- [RFC 4791 — CalDAV](https://datatracker.ietf.org/doc/html/rfc4791) — overview
- [RFC 6352 — CardDAV](https://datatracker.ietf.org/doc/html/rfc6352) — overview

## Key Concepts
- **Authoring over HTTP:** collections (folders), properties, and advisory locks — not just blob upload.
- **PROPFIND:** list properties / directory listing without downloading every body.
- **CalDAV / CardDAV:** iCalendar and vCard layered on WebDAV collections.
- **Same TLS/auth concerns:** as other [[HTTP module]] APIs.

## Technical Details
| Method | Purpose |
|--------|---------|
| **PROPFIND** | List properties / directory |
| **PROPPATCH** | Set properties |
| **MKCOL** | Create collection (folder) |
| **COPY / MOVE** | Server-side copy/move |
| **LOCK / UNLOCK** | Advisory locks |

- Typical URL:

```
https://webdav.example.com/remote.php/dav/files/user/
```

- Clients: macOS Finder, Windows Explorer, `rclone`, Nextcloud desktop.

```bash
curl -u user:pass -X PROPFIND \
  -H "Depth: 1" \
  https://webdav.example.com/dav/
```

- **CalDAV:** — iCalendar over WebDAV
- **CardDAV:** — vCard contacts

## Mistakes to Avoid
- **Mistake:** Exposing WebDAV with basic authentication on the public Internet…
- **Mistake:** Assuming PROPFIND equals GET on a directory
- **Mistake:** Using WebDAV as a general CDN origin for large static catalogs

## Pros/Cons or Trade-offs
- **Pro:** Familiar desktop drive mapping and collaborative authoring semantics (locks, properties).
- **Con:** S3-style APIs scale better for static assets and CDN distribution.
- **Con:** Path-traversal bugs in servers — keep software patched; require HTTPS.

## Comparison
- vs object storage (S3): WebDAV wins for authoring UX; object storage wins for scale and CDN.
- vs plain HTTP PUT: PROPFIND/LOCK give directory and concurrency semantics PUT alone lacks.


### Use cases
- Nextcloud/ownCloud file sync, shared corporate drives mapped as network folde…

- **Example:** A calendar app uses CalDAV so multiple devices share events with…
