[[HTTP module]] · [[TLS (Transport Layer Security)]] · [[TCP]]

# WebDAV

> Web Distributed Authoring and Versioning extends HTTP with methods for authoring files on remote servers — calendars (CalDAV) and contacts (CardDAV) build on the same MOVE/COPY/PROPFIND primitives.

---

## HTTP methods beyond GET/PUT

[RFC 4918](https://datatracker.ietf.org/doc/html/rfc4918) adds:

| Method | Purpose |
|--------|---------|
| **PROPFIND** | List properties / directory |
| **PROPPATCH** | Set properties |
| **MKCOL** | Create collection (folder) |
| **COPY / MOVE** | Server-side copy/move |
| **LOCK / UNLOCK** | Advisory locks |

## Typical URL

```
https://webdav.example.com/remote.php/dav/files/user/
```

Clients: macOS Finder, Windows Explorer, `rclone`, Nextcloud desktop.

## Example with curl

```bash
curl -u user:pass -X PROPFIND \
  -H "Depth: 1" \
  https://webdav.example.com/dav/
```

## CalDAV / CardDAV

- **CalDAV** ([RFC 4791](https://datatracker.ietf.org/doc/html/rfc4791)) — iCalendar over WebDAV
- **CardDAV** ([RFC 6352](https://datatracker.ietf.org/doc/html/rfc6352)) — vCard contacts

Same TLS and authentication concerns as [[HTTP module]] APIs.

## Security

- Require **HTTPS** ([[TLS (Transport Layer Security)]])
- Strong authentication; avoid basic auth on public Internet without MFA gateway
- **Path traversal** bugs in server implementations — keep software patched

## vs object storage

S3-style APIs scale better for static assets; WebDAV wins for **desktop drive mapping** and **collaborative authoring** semantics (locks, properties).

## Recall

- How does PROPFIND differ from HTTP GET on a directory?
- Why do calendar apps use CalDAV instead of plain PUT of `.ics` files?

## Sources

- [RFC 4918 — HTTP Extensions for WebDAV](https://datatracker.ietf.org/doc/html/rfc4918)
- [RFC 4791 — CalDAV](https://datatracker.ietf.org/doc/html/rfc4791)
