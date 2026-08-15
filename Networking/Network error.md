[[TCP]] [[UDP]] [[webSocket]] [[TLS (Transport Layer Security)]] [[DNS]] [[half-open connections]]

# Network error

> Network errors happen before or instead of an HTTP response — DNS, TCP, or TLS failed; you never got a status line.

## Interview Relevance

Interviewers want a layered mental model: DNS → TCP → TLS → HTTP. Distinguishing `ERR_*` / `ECONN*` from HTTP 502/503 shows you won’t chase the wrong hop.

## Sources

- [Chromium — Network Error Logging / net errors](https://chromium.googlesource.com/chromium/src/+/HEAD/net/base/net_error_list.h) — deep-dive
- [curl — Exit codes](https://curl.se/libcurl/c/libcurl-errors.html) — overview
- [MDN — TypeError (fetch)](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch) — overview

## Core Definition

A network error means the client never received an HTTP response because name resolution, connection setup, TLS handshake, or mid-flight peer reset failed first.

## Key Concepts

```txt
Client ──DNS──► TCP SYN ──TLS──► HTTP request ──► response
         │         │        │
         └── NXDOMAIN   timeout  cert fail  (network error zone)
```

| Signal | Meaning |
|--------|---------|
| `NS_BINDING_ABORTED` | Request cancelled (navigation, CORS preflight abort, user leave) |
| `ERR_CONNECTION_REFUSED` | RST / nothing listening |
| `ERR_CONNECTION_TIMED_OUT` | SYN or RTT exceeded |
| `ERR_NAME_NOT_RESOLVED` | DNS failure |
| `ERR_CERT_*` | TLS handshake failed |
| `ECONNRESET` / `EPIPE` | Peer closed mid-flight |

**Not network errors:** HTTP 502/503 from a proxy — TCP+TLS succeeded; the server returned a status.

## Technical Details

### Browser-side

```javascript
// fetch: TypeError on network fail; check err.name / err.cause
fetch(url).catch(e => console.error(e));
```

DevTools → **Network** tab → failed row shows `(failed) net::ERR_*`.

### Server / client CLI

```bash
curl -v https://api.example.com/health
# Times: DNS, connect, TLS, TTFB separately

mtr -rwzbc100 example.com
nc -zv host 443
openssl s_client -connect host:443 -servername host </dev/null
```

### Capture

```bash
sudo tcpdump -i any host api.example.com and port 443 -w trace.pcap
ss -tan state time-wait | wc -l   # exhaustion vs app bug
```

**Why split phases:** DNS fix ≠ firewall fix ≠ cert fix — measure each hop.

| Symptom | Check | Fix |
|---------|-------|-----|
| `NS_BINDING_ABORTED` | Cancelled navigation? CORS? | Not server bug if user navigated away; fix preflight |
| Intermittent mobile failures | TLS middleboxes | TLS 1.2+; proper cert chain |
| Works curl, fails browser | Mixed content, CORS, CSP | HTTPS everywhere; ACAO headers |
| Spike in timeouts | LB health, SYN queue | Scale backends; `somaxconn`; DDoS |
| Only one region | DNS geo / routing | GeoDNS; anycast; BGP path |

## Real-World Applications

Frontend “Network Error” banners, mobile flaky TLS, and on-call triage when users report outages that never hit application logs.

**Example:** Browser shows `ERR_NAME_NOT_RESOLVED` while `curl` from the server works — client DNS or ad-blocker path, not the API process.

## Pros/Cons or Trade-offs

- **Pro:** Phase-splitting (DNS/connect/TLS/HTTP) localizes fixes fast.
- **Con:** Browser messages are vague; same UI “network error” covers cancel, DNS, and RST.
- **Con:** Blind retries without idempotency can double-submit POSTs that partially succeeded.

## Comparison

- vs HTTP 4xx/5xx: application or proxy returned a response — not a transport failure.
- vs [[half-open connections]]: peer state desync can surface as reset/timeout network errors.
- vs CORS failures: often look like network errors in the UI but are browser policy after (or during) the request path.

## Mistakes to Avoid

- Chasing server logs for `NS_BINDING_ABORTED` when the client cancelled and the request never arrived.
- Treating ad blockers / corporate proxies as mysterious server bugs — they mimic network errors for blocked domains.
- Ignoring HTTP/2 GOAWAY / proxy idle timeouts that surface as vague resets.
- Blanket-retrying every network error without idempotency keys and dedupe.
