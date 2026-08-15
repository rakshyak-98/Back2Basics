[[mime type]] [[TCP]] [[HTTP]] [[Nginx Configuration]]

# Deflate (dflate)

> Lossless compression combining LZ77 dictionary matching + Huffman coding — raw DEFLATE is the payload inside gzip and zlib wrappers.

## Interview Relevance

Interviewers separate the **DEFLATE algorithm** from **gzip/zlib containers**, and expect you to know when HTTP compression saves bandwidth versus when it burns CPU or enables BREACH-class attacks.

## Sources

- [RFC 1951 — DEFLATE Compressed Data Format](https://www.rfc-editor.org/rfc/rfc1951) — deep-dive
- [RFC 1952 — GZIP file format](https://www.rfc-editor.org/rfc/rfc1952) — deep-dive
- [RFC 1950 — ZLIB Compressed Data Format](https://www.rfc-editor.org/rfc/rfc1950) — overview
- [MDN — Content-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding) — overview

## Core Definition

DEFLATE is a lossless bitstream (LZ77 + Huffman). gzip and zlib wrap that bitstream with headers and checksums; HTTP usually advertises `Content-Encoding: gzip`, not raw DEFLATE.

## Key Concepts

- **DEFLATE (RFC 1951):** the compression algorithm → exact bytes restored.
- **gzip / zlib:** container formats around DEFLATE → CRC/size (gzip) or Adler-32 (zlib).
- **Content-Encoding:** HTTP negotiation (`Accept-Encoding` / `Content-Encoding`) → one compression layer end-to-end.
- **Thresholds:** compress above ~1–2 KiB typically → tiny responses waste CPU.
- **Alternatives:** brotli / zstd often beat gzip on text → trade CPU and compatibility.

## Technical Details

```txt
HTTP Content-Encoding: gzip
  └─ gzip header + DEFLATE bitstream + CRC/size trailer

zlib (PNG, many libs)
  └─ zlib header + DEFLATE + Adler32
```

Properties: lossless; not especially parallel-friendly as a single stream; supports streaming chunk-by-chunk for HTTP.

```bash
echo 'hello world' | gzip | wc -c
echo 'hello world' | gzip -d

# Raw deflate (zlib wrapper) — interop testing
python3 -c "import zlib; print(len(zlib.compress(b'hello'*100)))"
```

```nginx
gzip on;
gzip_types application/json text/plain application/javascript;
gzip_min_length 1000;
gzip_comp_level 5;   # 1 fast .. 9 slow
```

```bash
curl -H 'Accept-Encoding: gzip' -v --compressed https://api.example.com/data
# --compressed auto-decompresses
```

```javascript
import compression from 'compression';
app.use(compression({ threshold: 1024 }));
```

**Why `gzip_min_length`:** compressing a 200-byte 404 costs CPU for negligible bytes saved.

| Symptom | Check | Fix |
|---------|-------|-----|
| Garbled response body | Double gzip; wrong Content-Encoding | One layer only; proxy decompress/recompress carefully |
| `ERR_CONTENT_DECODING_FAILED` | Truncated stream | Proxy buffer limits; disable gzip on broken path |
| High CPU | gzip level 9 on hot path | Lower level; offload to CDN; use zstd at edge |
| Android okhttp issues | Missing `Accept-Encoding` | Client must decode or disable gzip |

## Real-World Applications

API gateways and CDNs gzip JSON/HTML to cut bandwidth; static sites often serve precompressed `.gz`/`.br` assets.

**Example:** An API enables `gzip_comp_level 9` on every response — p99 latency rises on small payloads; drop to level 5 and set a minimum length.

## Pros/Cons or Trade-offs

- **Pro:** Large text/JSON responses shrink substantially with modest CPU at mid levels.
- **Con:** CPU on tiny or already-compressed bodies can increase latency.
- **Con:** Compression + secrets in the same response can enable BREACH-class attacks.

## Comparison

- vs gzip file: `.gz` has headers/trailer; raw DEFLATE alone confuses tools expecting gzip.
- vs brotli/zstd: better ratios on many text corpora; broader client support still favors gzip for some APIs.
- Related: [[mime type]], [[TCP]], [[Nginx Configuration]].

## Mistakes to Avoid

- Confusing DEFLATE with a `.gz` file — wrappers matter for interop.
- Double-compressing — precompressed assets plus on-the-fly gzip; set correct `Content-Encoding` once.
- Compressing JPEG/PNG/video again — already compressed; waste of CPU.
- Ignoring BREACH — gzip + secret in same body + attacker-controlled input; separate secrets or disable compression on sensitive endpoints.
