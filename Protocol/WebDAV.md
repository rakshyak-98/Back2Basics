[[Protocol]] [[HTTP module]] [[TLS (Transport Layer Security)]]

# WebDAV

> WebDAV (Web Distributed Authoring and Versioning) — HTTP extensions so clients can create, edit, move, and lock files on a server like a remote disk.

## Mental model

**Say it in one breath:** Plain HTTP is mostly read; WebDAV adds verbs (`PROPFIND`, `MKCOL`, `MOVE`, `COPY`, `LOCK`) so a browser, Finder, or sync client can treat a URL tree as a writable filesystem.

```txt
Client (OS mount / Nextcloud / cadaver)
        │  PROPFIND / PUT / MOVE / LOCK
        ▼
HTTP(S) server with WebDAV module (Apache mod_dav, nginx + dav, IIS)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **PROPFIND** | List collection + properties | “Directory listing is PROPFIND, not GET.” |
| --- | --- | --- |
| **MKCOL** | Make collection (folder) | “Folders are collections in WebDAV.” |
| **LOCK / UNLOCK** | Concurrency control | “Locks stop two editors stomping a file.” |
| **Depth header** | How deep PROPFIND walks | “Depth:1 vs infinity changes load a lot.” |
| **RFC 4918** | Core WebDAV spec | “It’s HTTP extensions, not a separate port.” |

### How the story goes

1. Client authenticates (Basic/Digest/Bearer over TLS).
2. PROPFIND discovers the tree; PUT uploads; MOVE/COPY rename.
3. LOCK around edit sessions when the client supports it.
4. Same TLS cert and reverse proxy path as any HTTPS application.

## Standard config / commands

```nginx
# nginx + dav module (sketch)
location /dav/ {
  dav_methods PUT DELETE MKCOL COPY MOVE;
  dav_ext_methods PROPFIND OPTIONS;
  create_full_put_path on;
  auth_basic "dav";
  auth_basic_user_file /etc/nginx/dav.htpasswd;
}
```

```bash
# CLI client
cadaver https://files.example.com/dav/
# ls / put local.txt / get remote.txt

curl -u user:pass -X PROPFIND https://files.example.com/dav/ \
  -H 'Depth: 1'
```

| Knob | Why it matters |

| TLS + auth | WebDAV without HTTPS leaks credentials and file bodies |
| --- | --- |
| `Range` / partial PUT | Some sync clients need server support |
| Max body size | Large uploads fail at proxy (`client_max_body_size`) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Mount works read-only | Methods blocked at proxy | Allow DAV methods; disable method filter |
| 401 loop | Auth scheme mismatch | Align Basic vs Digest vs SSO; fix HTTPS |
| Finder/Windows map fails | OPTIONS/PROPFIND blocked | Pass through DAV verbs; fix CORS only if browser |
| Upload 413 | Proxy body limit | Raise `client_max_body_size` / equivalent |
| Conflict / lost edits | No locks or stale lock | Enable LOCK; tune lock timeout |
| Slow folder open | Depth infinity PROPFIND | Cap Depth; paginate large collections |

## Gotchas

> [!WARNING]
> **WebDAV ≠ “just enable PUT”** — clients expect PROPFIND property XML and correct status codes (`207 Multi-Status`).

> [!WARNING]
> **Reverse proxies strip methods** — CDNs and WAFs often block PROPFIND/MOVE by default.

> [!WARNING]
> **Locking is advisory in practice** — broken clients ignore locks; design for conflict UI anyway.

## When NOT to use

- **Large-scale sync product** — purpose-built sync (rsync, object storage APIs, specialized sync protocol) scales better.
- **Simple application uploads** — plain multipart POST/S3 presign is enough.
- **Public anonymous write trees** — abuse magnet; use object storage with IAM.

## Related

[[HTTP module]] [[TLS (Transport Layer Security)]] [[ftp]] [[SCP (Secure Copy Protocol)]] [[nginx configuration structure]]
