[[mime type]] [[TCP]] [[HTTP]]

# Deflate (dflate)

> Lossless compression combining LZ77 dictionary matching + Huffman coding — raw DEFLATE is the payload inside gzip and zlib wrappers.

---

## Mental model

**DEFLATE** (RFC 1951) is the **algorithm**; **gzip** (RFC 1952) and **zlib** (RFC 1950) are **container formats** around it:

```txt
HTTP Content-Encoding: gzip
  └─ gzip header + DEFLATE bitstream + CRC/size trailer

zlib (PNG, many libs)
  └─ zlib header + DEFLATE + Adler32
```

Properties:
- **Lossless** — exact bytes restored
- **Not parallel-friendly** — single stream; brotli/zstd often beat it on text at cost of CPU
- **Streaming** — compress chunk-by-chunk for HTTP

**Service impact:** `gzip` on JSON/API saves bandwidth; CPU on small responses can **increase** latency — compress above ~1–2 KiB typically.

---

## Standard config / commands

### CLI compress/decompress

```bash
echo 'hello world' | gzip | wc -c
echo 'hello world' | gzip -d

# Raw deflate (zlib wrapper stripped) — interop testing
python3 -c "import zlib; print(len(zlib.compress(b'hello'*100)))"
```

### Nginx

```nginx
gzip on;
gzip_types application/json text/plain application/javascript;
gzip_min_length 1000;
gzip_comp_level 5;   # 1 fast .. 9 slow
```

### curl test

```bash
curl -H 'Accept-Encoding: gzip' -v --compressed https://api.example.com/data
# --compressed auto-decompresses
```

### Node / Express

```javascript
import compression from 'compression';
app.use(compression({ threshold: 1024 }));
```

**Why `gzip_min_length`:** compressing 200-byte 404 costs CPU for negligible bytes saved.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled response body | Double gzip; wrong Content-Encoding | One layer only; proxy decompress/recompress |
| `ERR_CONTENT_DECODING_FAILED` | Truncated stream | Proxy buffer limits; disable gzip on broken path |
| High CPU | gzip level 9 on hot path | Lower level; offload to CDN; use zstd at edge |
| Android okhttp issues | Missing `Accept-Encoding` | Client must decode or disable gzip |

---

## Gotchas

> [!WARNING]
> **DEFLATE ≠ gzip file** — `.gz` has headers; raw DEFLATE confuses tools expecting gzip.

> [!WARNING]
> **BREACH attack class** — gzip + secret in same body + attacker-controlled input — separate secrets or disable compression on sensitive endpoints.

> [!WARNING]
> **Precompressed static assets** — serve `.br`/`.gz` with correct headers; don't gzip twice.

---

## When NOT to use

Skip compression for **already compressed** media (JPEG, PNG, video) and **TLS 1.3 0-RTT** sensitive paths where timing matters more than bytes.

---

## Related

[[mime type]] [[response header]] [[Nginx Configuration]] [[TCP]]
