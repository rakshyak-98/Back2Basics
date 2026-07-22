[[TCP]] [[webSocket]] [[TLS (Transport Layer Security)]] [[CORS (Cross Origin Request Sharing)]]

# Network error

> Browser and client-visible failures when a request never completes cleanly — distinct from HTTP 4xx/5xx (those *did* complete).

---

## Mental model

**Network errors** happen **before or instead of** an HTTP response:

```txt
Client ──DNS──► TCP SYN ──TLS──► HTTP request ──► response
         │         │        │
         └── NXDOMAIN   timeout  cert fail  (network error zone)
```

Common codes/messages:

| Signal | Meaning |
|--------|---------|
| `NS_BINDING_ABORTED` | Request cancelled (navigation, CORS preflight abort, user leave) |
| `ERR_CONNECTION_REFUSED` | RST / nothing listening |
| `ERR_CONNECTION_TIMED_OUT` | SYN or RTT exceeded |
| `ERR_NAME_NOT_RESOLVED` | DNS failure |
| `ERR_CERT_*` | TLS handshake failed |
| `ECONNRESET` / `EPIPE` | Peer closed mid-flight |

**Not network errors:** HTTP 502/503 from a proxy — TCP+TLS succeeded; server returned status.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `NS_BINDING_ABORTED` | Cancelled navigation? CORS? | Not server bug if user navigated away; fix preflight |
| Intermittent mobile failures | TLS middleboxes | TLS 1.2+; proper cert chain |
| Works curl, fails browser | Mixed content, CORS, CSP | HTTPS everywhere; ACAO headers |
| Spike in timeouts | LB health, SYN queue | Scale backends; `somaxconn`; DDoS |
| Only one region | DNS geo / routing | GeoDNS; anycast; BGP path |

---

## Gotchas

> [!WARNING]
> **`NS_BINDING_ABORTED` is often client-side cancel** — don't chase server logs that never received the request.

> [!WARNING]
> **Ad blockers / corporate proxies** mimic network errors for blocked domains.

> [!WARNING]
> **HTTP/2 GOAWAY** can surface as vague network reset — check proxy idle timeouts.

---

## When NOT to use

Don't blanket-retry network errors without **idempotency** — POST may have partially succeeded; use idempotency keys and dedupe.

---

## Related

[[TCP]] [[UDP]] [[TLS (Transport Layer Security)]] [[DNS]] [[half-open connections]]
