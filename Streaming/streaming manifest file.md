[[Streaming]] [[Manifest (streaming)]] [[HLS]] [[DASH]] [[MPD]] [[flussonic]] [[How to attach stream to HTTP handlers]]

# streaming manifest file

> A streaming manifest lists segments and bitrates — if it embeds absolute origin URLs, rewrite them when you proxy so the player stays on your app host.

## Interview Relevance

Interviewers probe whether you can walk streaming manifest file end-to-end — not just name it. Signal fluency with **Manifest**, **Absolute URL**, **Relative URL**, **On-the-fly rewrite** and when you would pick a different path.

## Sources

- [Wikipedia — streaming manifest file](https://en.wikipedia.org/wiki/streaming_manifest_file) — overview

## Core Definition

General manifest shape and ABR fields live in [[Manifest (streaming)]]. This note is the **proxy URL rewrite** failure mode.

## Key Concepts

- **Manifest:** Playlist metadata (`.m3u8` / `.mpd`) — “Playback starts by fetching the manifest.”
- **Absolute URL:** Full `http://host/...` inside the file — “Absolute BaseURL makes the player skip our proxy.”
- **Relative URL:** Path without host — “Relative links keep requests on the same origin.”
- **On-the-fly rewrite:** Change body in the proxy, not on disk — “We translate URLs in memory; Flussonic’s file stays put.”
- **MPD refresh:** Live re-fetch of the MPD — “If Location stays absolute, refresh bypasses Node.”
- **CORS:** Browser cross-origin rules — “Leaving localhost for 127.0.0.1 breaks the page.”

### Why absolute URLs hurt (proxy case)

You load: `http://localhost:3000/flussonic/STREAM/index.mpd`

But the body may contain:

- MPD `<Location>http://127.0.0.1/...` or `http://FLUSSONIC_ORIGIN/...`
- HLS absolute `http://...` for child playlists / segments

Then Shaka (and friends) use **those** hosts for refreshes and segments → proxy, authentication, and CORS logic disappear. `127.0.0.1` may only exist **inside** the origin container — the user’s browser cannot reach it.

### Why rewrite fixes it

Node proxies the manifest, rewrites `${FLUSSONIC_ORIGIN}/...` → `/flussonic/...`, returns the **modified copy**. The player keeps talking to `localhost:3000`. Source on Flussonic is unchanged — translator in the middle.

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

See also [[How to attach stream to HTTP handlers]].

## Real-World Applications

General manifest shape and ABR fields live in [[Manifest (streaming)]]. This note is the **proxy URL rewrite** failure mode.

Used wherever streaming manifest file sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Public CDN with correct public BaseURL** — no application proxy; publish absolute **public** HTTPS URLs on purpose.
- **Con / skip when:** **Relative manifests already** — don’t add a rewrite layer for sport.
- **Con / skip when:** **WebRTC** — no HLS/DASH manifest; different stack ([[WebRTC]]).

## Comparison

- vs [[WebRTC]]: **WebRTC** — no HLS/DASH manifest; different stack ([[WebRTC]]).

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

- **Rewriting disk on Flussonic** — don’t; multi-tenant origins need the real host for other clients. Rewrite on the **response path**.
- **Only fixing the first MPD** — nested HLS media playlists often still ship absolute segment URLs.
- **String-replace too naive** — can corrupt tokens or XML; prefer URL-aware replace on known attributes (`BaseURL`, `Location`, URI=).
- **HTTPS page + HTTP absolute media** — mixed content blocks; rewrite to same-scheme relative paths.
