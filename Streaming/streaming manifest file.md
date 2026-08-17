[[Streaming]] [[Manifest (streaming)]] [[HLS]] [[DASH]] [[MPD]] [[flussonic]] [[How to attach stream to HTTP handlers]]

# streaming manifest file

> A streaming manifest lists segments and bitrates — if it embeds absolute origin URLs, rewrite them when you proxy so the player stays on your app host.

```txt
        streaming manifest ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk streaming manifest file end-to-end

## Sources
- [Wikipedia — streaming manifest file](https://en.wikipedia.org/wiki/streaming_manifest_file) — overview

## Key Concepts
- **Manifest:** Playlist metadata (`.m3u8` / `.mpd`)
- **Absolute URL:** Full `http://host/...` inside the file
- **Relative URL:** Path without host — “Relative links keep requests on the same origin.”
- **On-the-fly rewrite:** Change body in the proxy, not on disk
- **MPD refresh:** Live re-fetch of the MPD
- **CORS:** Browser cross-origin rules

### Why absolute URLs hurt (proxy case)

You load: `http://localhost:3000/flussonic/STREAM/index.mpd`

But the body may contain:

- **MPD `<Location>http://127.0.0.1/...`:** MPD `<Location>http://127.0.0.1/...` or `http://FLUSSONIC_ORIGIN/...`
- **HLS absolute:** HLS absolute `http://...` for child playlists / segments

- **Note:** Then Shaka (and friends) use **those** hosts for refreshes and segments → pro…

### Why rewrite fixes it

- **Note:** Node proxies the manifest, rewrites `${FLUSSONIC_ORIGIN}/...` → `/flussonic/.…


- **Core:** General manifest shape and ABR fields live in [[Manifest (streaming)]]

## Technical Details
```txt
Browser                    Node proxy                 Flussonic / origin
   │                            │                            │
   ├── GET /flussonic/…/index.mpd ──────────────────────────►│
   │◄── rewritten MPD (relative /app paths) ─────────────────┤
   │                            │                            │
   ├── GET /flussonic/…/seg.m4s  (stays on Node) ────────────►│
```

### Rewrite sketch (Node)

```js
// Fetch upstream, rewrite host, return to browser — do not mutate origin disk
const upstream = await fetch(`${FLUSSONIC_ORIGIN}${path}`)
let body = await upstream.text()
body = body.split(FLUSSONIC_ORIGIN).join('/flussonic')
// also map http://127.0.0.1:PORT → /flussonic when present
res.setHeader('Content-Type', upstream.headers.get('content-type'))
res.send(body)
```

### Sanity checks

```bash
# 1) What the browser should see — no foreign hosts
curl -s "http://localhost:3000/flussonic/STREAM/index.mpd" | grep -E 'http://|https://|BaseURL|Location'

# 2) Upstream raw (may contain absolute hosts)
curl -s "${FLUSSONIC_ORIGIN}/STREAM/index.mpd" | grep -E 'Location|BaseURL|http'
```

| Knob | Why it matters |
|------|----------------|
| Rewrite **MPD + nested HLS** | Child playlists can reintroduce absolute URLs |
| Preserve query tokens | Don’t strip signed URL query on rewrite |
| Correct `Content-Type` | Players sniff; keep `application/dash+xml` / `application/vnd.apple.mpegurl` |
| Live short cache | Don’t cache rewritten live MPD as immutable |
| Same-path segment proxy | Manifest rewrite alone is useless if segments 404 |

- See also [[How to attach stream to HTTP handlers]].

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| First frame OK, then fails on refresh | Absolute `<Location>` / BaseURL | Rewrite Location + BaseURL to app path |
| CORS errors mid-play | Network tab host ≠ page origin | Force relative URLs through proxy |
| `ERR_CONNECTION_REFUSED` to 127.0.0.1 | Manifest still has loopback | Map loopback → `/flussonic` |
| Segments 404 on Node | Only MPD rewritten | Proxy segment paths too |
| DRM / license works then media fails | Media GETs hit bare origin | Keep media on same origin as page policy |
| Works in curl, fails in Shaka | Shaka follows redirects/Location | Log every manifest URL Shaka requests |
| Intermittent wrong host | Partial string replace | Replace all origin variants (DNS name + IP) |

- **Mistake:** **Rewriting disk on Flussonic**
- **Mistake:** **Only fixing the first MPD**
- **Mistake:** **String-replace too naive**
- **Mistake:** **HTTPS page + HTTP absolute media**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Public CDN with correct public BaseURL**
- **Con / skip when:** **Relative manifests already**
- **Con / skip when:** **WebRTC**

## Comparison
- vs [[WebRTC]]: **WebRTC** — no HLS/DASH manifest; different stack ([[WebRTC]]).


### Use cases
- General manifest shape and ABR fields live in [[Manifest (streaming)]]

- Used wherever streaming manifest file sits in an ingest → package → CDN → pla…
